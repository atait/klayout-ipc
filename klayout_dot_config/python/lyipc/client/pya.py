''' These are functions specific to pya
    There is not necessarily any similarity with implementation in other languages
'''
from __future__ import print_function
from lygadgets import pya

import time
import os

# Makes it so that only one import is needed: lyipc.client.phidl will drop in for lyipc.client
from lyipc.client.general import *
from lyipc.client.dependent import *


def trace_pyainsert(layout, file):
    ''' Writes to file and loads in the remote instance whenever pya.Shapes.insert is called
        "layout" is what will be written to file and loaded there.

        Intercepts pya.Shapes.insert globally, not just for the argument "layout".
        This is because usually cells are generated before they are inserted into the layout,
        yet we would still like to be able to visualize their creation.
    '''
    pya.Shapes.old_insert = pya.Shapes.insert
    def new_insert(self, *args, **kwargs):
        retval = pya.Shapes.old_insert(self, *args, **kwargs)
        klayout_quickplot(layout, file, fresh=False)
        return retval
    pya.Shapes.insert = new_insert

