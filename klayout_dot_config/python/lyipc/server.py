import socket
import threading

import lyipc
from . import PORT, quickmsg, isGUI


global server_running
server_running = False
def toggle_server():
    if server_running:
        stop_serving()
    else:
        start_serving()


def stop_serving():
    global server_running
    server_running = False


def start_serving(port=PORT, threaded=True):
    ''' Basic idea here is to spawn a new thread that listens for messages sent by lyipc clients.
        The extra thread is needed to avoid blocking, so the GUI will keep working.
        This is not always desireable if you are using command-line server.

        threaded=None will make a best guess
    '''
    # Check for existing one
    global server_running
    if server_running:
        quickmsg('Server is already running')
        return
    server_running = True

    if threaded:
        server_thread = ServerThread(port)
        server_thread.start()
        return server_thread
    else:
        ServerThread.serve_loop(port)
        return None


class ServerThread(threading.Thread):
    def __init__(self, port=PORT):
        threading.Thread.__init__(self)
        self.port = port
        self.daemon = True

    def run(self):
        self.serve_loop(self.port)

    @staticmethod
    def serve_loop(port):
        # Create a TCP/IP socket and bind to a port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('', port)
        sock.bind(server_address)
        quickmsg(f'Starting server on port {port}')

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
                stop_serving()
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
            # Send command to interpreter
            from lyipc.interpreter import parse_command
            parse_command(payload)


if __name__ == '__main__':
    start_serving()

