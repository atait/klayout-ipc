''' The simplest interpreter you can imagine. Currently there are 4 commands and 0 queries

    Other ideas to implement:
        - query for value of variable as a string
        - execute arbitrary line of code, return its return value as a string
        - execute a macro
'''
from __future__ import print_function
from lyipc import quickmsg, isGSI
import lyipc.server
import os
import traceback

if not isGSI():
    raise RuntimeError('Non-klayout serving does not make sense')
import pya


def hard_load_layout(filename):
    ''' Swallow the error if the file is not completely written yet,
        or if the last file was not completely rendered.
        This doesn't seem to fatally affect the program
    '''
    main = pya.Application.instance().main_window()
    try:
        view = main.load_layout(filename, 0)
    except RuntimeError as err:
        if err.args[0].split()[0] in ['Stream', 'Unexpected']:
            print(err)
        else:
            raise


def parse_message(message):
    ''' Takes a message read from the socket and does something with it.

        The returned payload is not the same as what is returned from the called function:
        It is prepended with a status token and encoded (as a str) to be sent back over the socket
    '''
    return_val = None
    try:
        # if message == 'kill':
        #     quickmsg('Stopping server -- remote shutdown')
        #     pya.Application.exit(pya.Application.instance())

        if message == 'reload view':
            main = pya.Application.instance().main_window()
            main.cm_reload()

        elif message.startswith('load '):
            filename = message.split(' ')[1]
            filename = os.path.realpath(filename)
            quickmsg(filename)
            hard_load_layout(filename)

        else:
            quickmsg('Received {}'.format(message))

    except Exception:
        # Convert the stack trace to string to send to client
        payload = 'ERR ' + repr(traceback.format_exc())  # repr makes it so multi-line strings go as one string
    else:
        # Tell the client that it worked
        payload = 'ACK ' + str(return_val)
    return payload
