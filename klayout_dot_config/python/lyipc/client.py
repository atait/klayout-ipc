''' The client is designed to run in either python or klayout's interpreter
'''
from __future__ import print_function
import socket
from lyipc import PORT, isGSI
import os
import time
import sys
from functools import lru_cache, wraps


if not isGSI():
    # print('Warning: pya will not be available')
    import PyQt5.QtNetwork
else:
    import pya


def reload():
    send('reload view')


fast_realpath = lru_cache(maxsize=4)(os.path.realpath)  # Since the argument is going to be the same every time
def load(filename):
    filename = fast_realpath(filename)
    # TODO: use a temporary file
    send(f'load {filename}')


def kill():
    send('kill')


def send(message='ping 1234', port=PORT):
    ''' Sends a raw message

        Trick here is that PyQt5 does not do automatic str<->byte encoding, but pya does. Also something weird with the addresses
    '''
    payload = message + '\r\n'
    if isGSI():
        psock = pya.QTcpSocket()
        ha = 'localhost'
    else:
        psock = PyQt5.QtNetwork.QTcpSocket()
        ha = PyQt5.QtNetwork.QHostAddress.LocalHost
        payload = payload.encode()

    psock.connectToHost(ha, port)
    if psock.waitForConnected():
        psock.write(payload)
        if psock.waitForReadyRead(3000):
            ret = psock.readLine()
            if not isGSI():
                ret = bytes(ret).decode('utf-8')
            handle_query(ret)
        else:
            raise Exception('Not acknowledged')
    else:
        print(f'Connection Fail! (tried {ha}:{port})')
    # psock.close()


def handle_query(retString):
    ''' Extra check that there is handshaking. Now handles error
    '''
    if retString.startswith('ACK '):
        return retString[4:]
    elif retString.startswith('ERR '):
        traceback_repr = retString[4:]
        # The traceback is sent as a single line as a string repr. Now convert back to multi-line
        traceback_str = traceback_repr.encode("utf-8").decode('unicode_escape').strip("'")
        print('\n' + traceback_str)
        print('^ Server-side error ^')
        sys.exit(1)



def trace_pyainsert(layout, file, write_load_delay=0.01):
    ''' Writes to file and loads in the remote instance whenever pya.Shapes.insert is called
        "layout" is what will be written to file and loaded there.

        Intercepts pya.Shapes.insert globally, not just for the argument "layout".
        This is because usually cells are generated before they are inserted into the layout,
        yet we would still like to be able to visualize their creation.
    '''
    import pya
    pya.Shapes.old_insert = pya.Shapes.insert
    def new_insert(self, *args, **kwargs):
        retval = pya.Shapes.old_insert(self, *args, **kwargs)
        layout.write(file)
        time.sleep(write_load_delay)
        load(file)
        return retval
    pya.Shapes.insert = new_insert


def trace_phidladd(device, file, write_load_delay=0.01):
    ''' Writes to file and loads in the remote instance whenever phidl.Device.add is called
    '''
    import phidl
    phidl.device_layout.Device.old_add = phidl.device_layout.Device.add
    def new_add(self, *args, **kwargs):
        retval = phidl.device_layout.Device.old_add(self, *args, **kwargs)
        device.write_gds(file)
        time.sleep(write_load_delay)
        load(file)
        return retval
    phidl.device_layout.Device.add = new_add
