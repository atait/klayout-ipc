''' Server is designed to run from klayout GSI, usually in GUI mode

    Current state: only way to stop serving is close the application.
'''
from __future__ import print_function

import socket
import lyipc
from lygadgets import message, isGSI

if not isGSI():
    raise RuntimeError('Non-klayout serving does not make sense')
import pya


# As of now, port is hard coded and there is no way to stop it besided closing the app
# We have to make sure that a second server doesn't come along and clash
global __active_server
__active_server = None
def run_server():
    global __active_server
    if __active_server is None:
        __active_server = KlayoutServer()
    return __active_server


class KlayoutServer(pya.QTcpServer):
    def new_connection(self):
        from lyipc.interpreter import parse_message
        # Handle incoming connection
        connection = self.nextPendingConnection()
        msg = 'null'
        while connection.isOpen() and connection.state() == pya.QTcpSocket.ConnectedState:
            if connection.canReadLine():
                payload = connection.readLine()
                msg = payload.rstrip('\n').rstrip('\r')
                response = parse_message(msg)
                connection.write(response)
                connection.disconnectFromHost()
            else:
                connection.waitForReadyRead(500)
        signal = pya.qt_signal("disconnected()")
        slot = pya.qt_slot("deleteLater()")
        pya.QObject.connect(connection, signal, connection, slot)


    def __init__(self, port=lyipc.PORT, parent=None):
        pya.QTcpServer.__init__(self, parent)
        localhost = pya.QHostAddress()
        self.listen(localhost, port)
        self.newConnection(self.new_connection)
        message('Server initialized with {}, {}'.format(localhost, port))
