from __future__ import print_function
import socket
from lyipc import PORT, isGSI


if not isGSI():
    print('Warning: pya will not be available')
    try:
        from PyQt5.QtNetwork import QTcpSocket
    except ImportError as e:
        print('No PyQt5 found. You have to run this script from klayout\'s interpreter')
else:
    from pya import QTcpSocket

def reload():
    send('reload view')

def load(filename):
    send(f'load {filename}')


def kill():
    send('kill')


def send(message='ping 1234', port=PORT):
    ''' Sends a raw message '''
    payload = message + '\r\n'
    psock = QTcpSocket()
    ha = 'localhost'
    # import pdb; pdb.set_trace()
    psock.connectToHost(ha, port)
    if psock.waitForConnected():
        psock.write(payload)#.encode())
        if not psock.waitForReadyRead(3000) or not psock.readLine().startswith('ACK'):
            raise Exception('Not acknowledged')
    else:
        print(f'Connection Fail! (tried {ha}:{port})')
