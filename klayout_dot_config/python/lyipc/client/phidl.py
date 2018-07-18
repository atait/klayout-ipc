''' These are functions specific to phidl '''
from __future__ import print_function
import phidl

from .general import load, reload, kill, diff
import time
import os
from functools import wraps


def klayout_quickplot(device, file, fresh=False, write_load_delay=0.01):
    ''' Does the write, wait, and load all in one.
        The fresh argument determines whether to load (True) or reload (False)

        TODO:
            Make compatible with pya
    '''
    device.write_gds(file)
    time.sleep(write_load_delay)
    if fresh:
        load(file)
    else:
        reload()


def generate_display_function(default_device, default_file):
    ''' A quick way to configure quickplotter into a brief command

        Usage::
            TOP = Device()
            kqp = make_display_function('debugging.gds', TOP)
            ...
            kqp()
    '''
    default_file = os.path.realpath(default_file)
    @wraps(klayout_quickplot)
    def k_quick(device=default_device, file=default_file, **kwargs):
        klayout_quickplot(device, file, **kwargs)
    return k_quick


def trace_phidladd(device, file, write_load_delay=0.01):
    ''' Writes to file and loads in the remote instance whenever phidl.Device.add is called
    '''
    import phidl
    phidl.device_layout.Device.old_add = phidl.device_layout.Device.add
    def new_add(self, *args, **kwargs):
        retval = phidl.device_layout.Device.old_add(self, *args, **kwargs)
        device.write_gds(file)
        time.sleep(write_load_delay)
        load(file)
        return retval
    phidl.device_layout.Device.add = new_add
