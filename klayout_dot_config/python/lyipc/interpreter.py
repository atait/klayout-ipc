# The simplest interpreter you can imagine
from lyipc import quickmsg, isGUI
import lyipc.server


def parse_command(cmdStr):
    if cmdStr == 'kill':
        quickmsg('Stopping server -- remote shutdown')
        import pya
        pya.Application.exit()
    if cmdStr == 'reload view' and isGUI():
        import pya
        pya.Application.instance().main_window().cm_reload()
    else:
        quickmsg(f'Received {cmdStr}')