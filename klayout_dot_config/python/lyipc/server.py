import socket
import time
import sys
import os
from . import PORT, quickmsg


global server_running
server_running = False
def toggle_server():
    if server_running:
        stop_serving()
    else:
        start_serving()


def start_serving(port=PORT):
    # Stop an existing one
    global server_running
    if server_running:
        stop_serving()
    server_running = True
    
    # Create a TCP/IP socket and bind to a port
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', port)
    sock.bind(server_address)
    quickmsg(f"Starting server on port {port}")

    # Listen for incoming connections
    sock.settimeout(1.0)  # this makes sure that it doesn't block indefinitely. We have to check if the server was told to stop
    sock.listen(1)
    while server_running:
        try:
            # Wait for a connection
            connection, client_address = sock.accept()
        except socket.timeout:
            print('timeout')
            continue
        except KeyboardInterrupt:                           # TODO there is no interrupt in GUI mode
            quickmsg('Stopping server -- KeyboardInterrupt')
            return

        # Connection has happened.
        with connection:
            # Read the payload in chunks
            payload = ''
            while True:
                try:
                    data = connection.recv(16).decode()
                except:
                    payload += '...Corrupted'
                    raise IOError(f'Socket data corrupted: {payload}')
                if data:
                    payload += data
                else:
                    break
            # Let the client know we are good
            connection.sendall('ACK'.encode())
        parse_remote_command(payload)
    quickmsg('Stopping server -- program request')


def parse_remote_command(cmdStr):
    quickmsg(f'received {cmdStr}')
    if cmdStr == 'kill':
        quickmsg('Stopping server -- remote shutdown')
        stop_serving()


def stop_serving():
    global server_running
    server_running = False


if __name__ == '__main__':
    start_serving()

