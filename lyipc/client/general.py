''' These are functions that are independent of the layout package '''
from __future__ import print_function
from lyipc.client import send
from lyipc.client.remotehost import is_host_remote, ship_file
from functools import lru_cache
import os
import time
from functools import wraps


def reload():
    send('reload view')


fast_realpath = lru_cache(maxsize=4)(os.path.realpath)  # Since the argument is going to be the same every time
def load(filename, mode=None):
    '''
        Modes are
        - 0 (default): replacing the current layout view
        - 1: making a new view
        - 2: adding the layout to the current view (mode 2)
    '''
    # if it's remote, we have to ship the file over first
    filename = fast_realpath(filename)
    if is_host_remote():
        filename = ship_file(filename)  # filename has changed to reflect what it is on the remote system
    tokens = ['load', filename]
    if mode is not None:
        tokens.append(str(mode))
    send(' '.join(tokens))


def kill():
    send('kill')


def view(cellname):
    send('cellview ' + str(cellname))


def diff(file1, file2):
    pass  # TODO


class ServerSideError(RuntimeError):
    pass
