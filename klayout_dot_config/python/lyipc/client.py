from __future__ import print_function
import socket
from lyipc import PORT, isGSI


if not isGSI():
    print('Warning: pya will not be available')
else:
    import pya

def reload():
    send('reload view')

def load(filename):
    send(f'load {filename}')


def kill():
    send('kill')


def send(message='ping 1234', port=PORT):
    ''' Sends a raw message '''
    if isGSI():
        psock = pya.QTcpSocket()
    else:
        raise NotImplementedError('non-GSI')
    ha = 'localhost'
    # import pdb; pdb.set_trace()
    psock.connectToHost(ha, port)
    if psock.waitForConnected():
        psock.write(message + '\r\n')
        x = psock.waitForReadyRead(3000)
        ret = psock.readLine()
        # if psock.readBytes() == 0 or ret != 'ACK':
        #     raise Exception('Not acknowledged')
    else:
        print(f'Connection Fail! (tried {ha}:{port})')
