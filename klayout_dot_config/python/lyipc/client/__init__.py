''' This package contains a core for communicating with the server (in this file)
    and an API that is exposed to client-side layout programs. Modules are organized based on package.
        - general.py is package independent
        - pya.py is klayout specific
        - phidl.py is phidl specific
'''
from __future__ import print_function
from lyipc import isGSI, PORT


if not isGSI():
    # print('Warning: pya will not be available')
    import PyQt5.QtNetwork
    from PyQt5.QtNetwork import QTcpSocket
    localhost = PyQt5.QtNetwork.QHostAddress.LocalHost
else:
    import pya
    from pya import QTcpSocket
    localhost = pya.QHostAddress()


def send(message='ping 1234', port=PORT):
    ''' Sends a raw message

        Trick here is that PyQt5 does not do automatic str<->byte encoding, but pya does. Also something weird with the addresses
    '''
    payload = message + '\r\n'
    psock = QTcpSocket()
    if not isGSI():
        payload = payload.encode()
    psock.connectToHost(localhost, port)
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
        print(f'Connection Fail! (tried {localhost}:{port})')
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


from .general import *
