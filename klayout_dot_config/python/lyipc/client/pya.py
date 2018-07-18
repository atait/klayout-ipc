''' These are functions specific to pya '''
from __future__ import print_function
import pya

from .general import load, reload, kill, diff
import time
import os
from functools import wraps


def klayout_quickplot(cell_or_layout, file, fresh=False, write_load_delay=0.01):
    ''' Does the write, wait, and load all in one.
        The fresh argument determines whether to load (True) or reload (False)
    '''
    cell_or_layout.write(file)
    time.sleep(write_load_delay)
    if fresh:
        load(file)
    else:
        reload()


def generate_display_function(default_cell_or_layout, default_file):
    ''' A quick way to configure quickplotter into a brief command

        Usage::
            TOP = Layout()
            kqp = make_display_function('debugging.gds', TOP)
            ...
            kqp()
    '''
    default_file = os.path.realpath(default_file)
    @wraps(klayout_quickplot)
    def k_quick(cell_or_layout=default_cell_or_layout, file=default_file, **kwargs):
        klayout_quickplot(cell_or_layout, file, **kwargs)
    return k_quick


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

