''' This package contains a core for communicating with the server (in this file)
    and an API that is exposed to client-side layout programs. Modules are organized based on package.
        - general.py is package independent
        - pya.py is klayout specific
        - phidl.py is phidl specific
'''
from __future__ import print_function

import lyipc
from lygadgets import isGSI
import socket
import os
from lyipc.client.remotehost import set_target_hostname, get_target_hostname

# Determine which socket class to use
if not isGSI():
    # print('Warning: pya will not be available')
    import sys
    if sys.version_info[0] == 2:
        raise Exception('Please use python >= 3.1 with lyipc for the time being')
    elif sys.version_info[0] == 3:
        import PyQt5.QtNetwork
        from PyQt5.QtNetwork import QTcpSocket
        # localhost = '127.0.0.1'
else:
    from lygadgets import pya
    from pya import QTcpSocket
    # localhost = 'localhost'


def send(message='ping 1234', port=None):
    ''' Sends a raw message

        Trick here is that PyQt5 does not do automatic str<->byte encoding, but pya does. Also something weird with the addresses
    '''
    if port is None:
        port = lyipc.PORT
    payload = message + '\r\n'
    psock = QTcpSocket()
    if not isGSI():
        payload = payload.encode()
    psock.connectToHost(get_target_hostname(incl_user=False), port)
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
        print('Connection Fail! (tried {}:{})'.format(get_target_hostname(incl_user=False), port))
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
        raise ServerSideError(traceback_str + '^ Server-side error ^')


from lyipc.client.general import *
from lyipc.client.dependent import *

# for easy access, just: from lyipc.client import kqp
kqp = generate_display_function(None, 'debugging.gds')

