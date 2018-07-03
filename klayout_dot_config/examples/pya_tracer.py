''' Automatically launches a subprocess klayout and drops into debug shell
'''

import lyipc.client as ipc
import os
import time
import numpy as np
from functools import partial

import pya
import sys
pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd)

debug_file = os.path.realpath('debuglobal.gds')


def intercept_pyainsert(layout, write_load_delay=0.01):
    ''' Writes to file and loads in the remote instance.
        "layout" is what will be written to file and loaded there.

        Intercepts pya.Shapes.insert globally, not just for the argument "layout".
        This is because usually cells are generated before they are inserted into the layout,
        yet we would still like to be able to visualize their creation.
    '''
    pya.Shapes.old_insert = pya.Shapes.insert
    def new_insert(self, *args, **kwargs):
        retval = pya.Shapes.old_insert(self, *args, **kwargs)
        layout.write(debug_file)
        time.sleep(write_load_delay)
        ipc.load(debug_file)
        return retval
    pya.Shapes.insert = new_insert


def simple_create():
    layout = pya.Layout()
    intercept_pyainsert(layout, 0.02)
    layout.dbu = 0.001
    TOP = layout.create_cell('TOP')
    l1 = layout.insert_layer(pya.LayerInfo(1, 0))
    l2 = layout.insert_layer(pya.LayerInfo(2, 0))

    for i in range(21):
        for j in range(21):
            box = pya.DBox(0, 0, 10, 10)
            box.move(15 * i, 15 * j)
            TOP.shapes(l1).insert(box)
    TOP.shapes(l2).insert(pya.DBox(0,0,500,500))


def tough_create():
    layout = pya.Layout()
    intercept_pyainsert(layout, 1e-4)
    layout.dbu = 0.001
    TOP = layout.create_cell('TOP')
    l1 = layout.insert_layer(pya.LayerInfo(1, 0))
    l2 = layout.insert_layer(pya.LayerInfo(2, 0))

    for i in range(51):
        for j in range(51):
            box = pya.DBox(0, 0, 10, 10)
            box.move(15 * i, 15 * j)
            TOP.shapes(l1).insert(box)
    TOP.shapes(l2).insert(pya.DBox(0,0,1000,1000))


simple_create()
