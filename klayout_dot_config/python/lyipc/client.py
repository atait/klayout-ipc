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
    if psock.waitForConnected(1000):
        print('Connection made')
        psock.write(message + '\r\n')
        psock.waitForReadyRead(3000)
        ret = psock.readAll()
        # if psock.readBytes() == 0 or ret != 'ACK':
        #     raise Exception('Not acknowledged')
    else:
        print('Connection Fail!')

# send()
