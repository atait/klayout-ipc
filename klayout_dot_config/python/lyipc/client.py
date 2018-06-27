from __future__ import print_function
import socket
from lyipc import PORT


def remotewrite():
    send('reload view')


def remoteload(filename):
    send(f'load {filename}')


def kill():
    send('kill')


def send(message='ping 1234', port=PORT):
    ''' Sends a raw message '''
    import pya
    psock = pya.QTcpSocket()
    psock.connectToHost('localhost', port)
    if psock.waitForConnected():
        print('Connection made')
        psock.write(message + '\r\n')
        if not psock.waitForReadyRead(3000) or psock.readAll() != 'ACK':
            raise Exception('Not acknowledged')

send()
