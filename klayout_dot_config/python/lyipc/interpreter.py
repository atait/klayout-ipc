''' The simplest interpreter you can imagine. Currently there are 4 commands and 0 queries

    Other ideas to implement:
        - query for value of variable as a string
        - execute arbitrary line of code, return its return value as a string
        - execute a macro
'''
from __future__ import print_function
from lygadgets import message, isGSI
import lyipc.server
import os
import traceback

if not isGSI():
    raise RuntimeError('Non-klayout serving does not make sense')
import pya


def quiet_load_layout(filename, mode=0):
    ''' Swallow the error if the file is not completely written yet,
        or if the last file was not completely rendered.
        This doesn't seem to fatally affect the program.

        Modes are
        - 0 (default): replacing the current layout view
        - 1: making a new view
        - 2: adding the layout to the current view (mode 2)
    '''
    main = pya.Application.instance().main_window()
    try:
        view = main.load_layout(filename, mode)
    except RuntimeError as err:
        if err.args[0].split()[0] in ['Stream', 'Unexpected']:
            print(err)
        else:
            raise


def parse_message(msg):
    ''' Takes a msg read from the socket and does something with it.

        Careful of name conflict with lygadgets.

        The returned payload is not the same as what is returned from the called function:
        It is prepended with a status token and encoded (as a str) to be sent back over the socket
    '''
    return_val = None
    tokens = msg.split(' ')
    try:
        # if msg == 'kill':
        #     message('Stopping server -- remote shutdown')
        #     pya.Application.exit(pya.Application.instance())

        if tokens == ['reload', 'view']:
            main = pya.Application.instance().main_window()
            main.cm_reload()

        elif tokens[0] == 'load':
            filename = os.path.realpath(tokens[1])
            message(filename)
            if len(tokens) > 2:
                mode = int(tokens[2])
                quiet_load_layout(filename, mode)
            else:
                quiet_load_layout(filename)

        else:
            message('Received {}'.format(msg))

    except Exception:
        # Convert the stack trace to string to send to client
        payload = 'ERR ' + repr(traceback.format_exc())  # repr makes it so multi-line strings go as one string
    else:
        # Tell the client that it worked
        payload = 'ACK ' + str(return_val)
    return payload
