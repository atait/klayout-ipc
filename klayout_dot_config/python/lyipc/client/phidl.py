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
from lyipc.client.general import *
from lyipc.client.dependent import *


def trace_phidladd(device, file):
    ''' Writes to file and loads in the remote instance whenever phidl.Device.add is called
    '''
    phidl.device_layout.Device.old_add = phidl.device_layout.Device.add
    def new_add(self, *args, **kwargs):
        retval = phidl.device_layout.Device.old_add(self, *args, **kwargs)
        klayout_quickplot(device, file, fresh=False)
        return retval
    phidl.device_layout.Device.add = new_add
