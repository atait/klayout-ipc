# The simplest interpreter you can imagine
from lyipc import quickmsg, isGSI
import lyipc.server
import os

if isGSI():
    import pya


def hard_load_layout(filename):
    ''' Swallow the error if the file is not completely written yet.
        This doesn't seem to adversely affect the program
    '''
    main = pya.Application.instance().main_window()
    try:
        view = main.load_layout(filename, 0)
    except RuntimeError as err:
        if err.args[0].split()[0] in ['Stream', 'Unexpected']:
            print(err)
        else:
            raise


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
        quickmsg(filename)
        hard_load_layout(filename)
    else:
        quickmsg(f'Received {cmdStr}')