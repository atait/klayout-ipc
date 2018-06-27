# The simplest interpreter you can imagine
from lyipc import quickmsg, isGSI
import lyipc.server
import os

if isGSI():
    import pya

def parse_command(cmdStr):
    if not isGSI():
        print(f'Received {cmdStr}')
        return

    # if cmdStr == 'kill':
    #     quickmsg('Stopping server -- remote shutdown')
    #     pya.Application.exit(pya.Application.instance())

    elif cmdStr == 'reload view':
        main = pya.Application.instance().main_window()
        main.cm_reload()

    elif cmdStr.startswith('load '):
        filename = cmdStr.split(' ')[1]
        filename = os.path.realpath(filename)
        main = pya.Application.instance().main_window()
        quickmsg(filename)
        view = main.load_layout(filename, 0)

    else:
        quickmsg(f'Received {cmdStr}')