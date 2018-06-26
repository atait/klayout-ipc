import socket
from . import PORT


def remotewrite(filename):
    pass


def send(message='ping 1234', port=PORT):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', port)
    try:
        sock.connect(server_address)
        with sock:
            sock.sendall(message.encode())
            # TODO: check for acknowlegement by server
    except:
        print('Fail in send')
