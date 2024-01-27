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


def send(message='ping 1234', port=None, timeout=3):
    ''' Sends a raw message
    '''
    if port is None:
        port = lyipc.PORT
    payload = message + '\r\n'
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        sock.connect((get_target_hostname(incl_user=False), port))
        sock.sendall(payload.encode())
        data = sock.recv(1024).decode()
    return handle_query(data)


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

