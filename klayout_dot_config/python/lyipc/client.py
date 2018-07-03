''' The client is designed to run in either python or klayout's interpreter
'''
from __future__ import print_function
import socket
from lyipc import PORT, isGSI
import os
from functools import lru_cache


if not isGSI():
    # print('Warning: pya will not be available')
    try:
        import PyQt5.QtNetwork
    except ImportError as e:
        print('Warning: No PyQt5 found. You have to run this script from klayout\'s interpreter')
else:
    import pya


def reload():
    send('reload view')


fast_realpath = lru_cache(maxsize=4)(os.path.realpath)  # Since the argument is going to be the same every time
def load(filename):
    filename = fast_realpath(filename)
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
    ''' For now all this does is make sure there is handshaking '''
    if retString != 'ACK':
        raise Exception('Not acknowledged, instead: ' + retString)
