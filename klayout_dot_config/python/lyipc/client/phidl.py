''' These are functions specific to phidl.
    There is not necessarily any similarity with implementation in other languages
'''
from __future__ import print_function
import phidl
from phidl import Device

import time
import os
from contextlib import contextmanager
from functools import wraps

# Makes it so that only one import is needed: lyipc.client.phidl will drop in for lyipc.client
from .general import *
from .dependent import *


def trace_phidladd(device, file):
    ''' Writes to file and loads in the remote instance whenever phidl.Device.add is called
    '''
    phidl.device_layout.Device.old_add = phidl.device_layout.Device.add
    def new_add(self, *args, **kwargs):
        retval = phidl.device_layout.Device.old_add(self, *args, **kwargs)
        klayout_quickplot(device, file, fresh=False)
        return retval
    phidl.device_layout.Device.add = new_add


@contextmanager
def save_or_visualize(device_name=None, out_file=None):
    ''' Handles a conditional write to file or send over lyipc connection.
        The context manager yields a new empty Device.
        The context block then modifies that device by adding references to it. It does not need to return anything.
        Back to the context manager, the Device is saved if out_file is not None, or it is sent over ipc

        Example::

            with save_or_visualize(out_file='my_box.gds') as D:
                r = D << phidl.geometry.rectangle(size=(10, 10), layer=1)
                r.movex(20)

        will write the device with a rectangle to a file called 'my_box.gds' and do nothing with lyipc.
        By changing out_file to None, it will send an ipc load command instead of writing to a permanent file,
        (Although ipc does write a file to be loaded by klayout, it's name or persistence is not guaranteed.)
    '''
    if device_name is None:
        CELL = Device()
    else:
        CELL = Device(device_name)
    yield CELL
    if out_file is None:
        klayout_quickplot(CELL, 'debugging.gds', fresh=True)
    else:
        CELL.write_gds(out_file)


def contained_geometry(func):
    '''
        Converts a function that takes a Device argument to one that takes a filename argument.
        This is used to develop fixed geometry creation blocks and then save them as reference files.
        Bad idea to try to use this in a library or call it from other functions.

        func should take *only one* argument that is a Device, modify that Device, and return nothing.

        It's sort of a decorator version of save_or_visualize.
        When called with a None argument, it will use klayout_quickplot.

        Example::

            @contained_geometry
            def boxer(D):
                r = D << phidl.geometry.rectangle(size=(10, 10), layer=1)
                r.movex(20)

        Usage::

            boxer()  # displays in klayout over ipc
            boxer('temp.gds')  # saves to file instead

    '''
    @wraps(func)
    def geometry_container(out_file=None):
        with save_or_visualize(out_file=out_file) as TOP:
            func(TOP)
    return geometry_container
