# The simplest interpreter you can imagine
from lyipc import quickmsg, isGUI
import lyipc.server
import os

def parse_command(cmdStr):
    if cmdStr == 'kill':
        quickmsg('Stopping server -- remote shutdown')
        import pya
        pya.Application.exit()
    elif cmdStr == 'reload view' and isGUI():
        import pya
        main = pya.Application.instance().main_window()
        main.cm_reload()
    elif cmdStr.startswith('load '):
        filename = cmdStr.split(' ')[1]
        filename = os.path.realpath(filename)
        import pya
        main = pya.Application.instance().main_window()
        view = main.load_layout(filename, 1)
    else:
        quickmsg(f'Received {cmdStr}')