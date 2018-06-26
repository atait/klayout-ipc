# The simplest interpreter you can imagine
from lyipc import quickmsg
import lyipc.server


def parse_command(cmdStr):
    if cmdStr == 'kill':
        quickmsg('Stopping server -- remote shutdown')
        lyipc.server.stop_serving()
    else:
        quickmsg(f'Received {cmdStr}')