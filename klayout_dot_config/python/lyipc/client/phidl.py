''' These are functions specific to phidl

    By importing this module, the client.general module learns how to write phidl.Device
'''
from __future__ import print_function
import phidl

import time
import os

from .dependent import klayout_quickplot


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
