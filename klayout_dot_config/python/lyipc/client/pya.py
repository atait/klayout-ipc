''' These are functions specific to pya

    By importing this module, the client.general module learns how to write pya.Cell and pya.Layout
'''
from __future__ import print_function
import pya

import time
import os

from .dependent import klayout_quickplot


def trace_pyainsert(layout, file, write_load_delay=0.01):
    ''' Writes to file and loads in the remote instance whenever pya.Shapes.insert is called
        "layout" is what will be written to file and loaded there.

        Intercepts pya.Shapes.insert globally, not just for the argument "layout".
        This is because usually cells are generated before they are inserted into the layout,
        yet we would still like to be able to visualize their creation.
    '''
    pya.Shapes.old_insert = pya.Shapes.insert
    def new_insert(self, *args, **kwargs):
        retval = pya.Shapes.old_insert(self, *args, **kwargs)
        layout.write(file)
        time.sleep(write_load_delay)
        load(file)
        return retval
    pya.Shapes.insert = new_insert

