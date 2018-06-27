''' Used QTcpServer
    Current state: only way to stop serving is close the application
'''
import socket
import pya

import lyipc
from lyipc import PORT, quickmsg

class KlayoutServer(pya.QTcpServer):
    def new_connection(self):
        try:
            # Handle incoming connection
            connection = self.nextPendingConnection()
            payload = ''
            while connection.isOpen() and connection.state() == pya.QTcpSocket.ConnectedState:
                # connection.waitForReadyRead(1000)
                if connection.canReadLine():
                    line = connection.readLine()
                    payload = line
                    connection.write('ACK')
                else:
                    connection.waitForReadyRead(500)

            quickmsg('payload=', payload)

            # automatically delete when disconnected
            connection.disconnectFromHost()
            signal = pya.qt_signal("disconnected()")
            slot = pya.qt_slot("deleteLater()")
            pya.QObject.connect(connection, signal, connection, slot)

            # Do something with what was received
            from lyipc.interpreter import parse_command
            parse_command(payload)
        except Exception as ex: 
            print("ERROR " + str(ex))

    def __init__(self, port=PORT, parent=None):
        pya.QTcpServer.__init__(self, parent)
        ha = pya.QHostAddress()
        self.listen(ha, port)
        self.newConnection(self.new_connection)

KlayoutServer()

def start_serving():
    print('a')

