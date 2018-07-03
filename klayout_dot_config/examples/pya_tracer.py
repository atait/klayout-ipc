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

# Hijack pya
layout = pya.Layout()
pya.Shapes.old_insert = pya.Shapes.insert
def new_insert(self, *args, **kwargs):
    retval = pya.Shapes.old_insert(self, *args, **kwargs)
    layout.write(debug_file)
    time.sleep(0.01)
    ipc.load(debug_file)
    return retval
pya.Shapes.insert = new_insert


def simple_create():
    dbu = layout.dbu = 0.001
    TOP = layout.create_cell('TOP')
    l1 = layout.insert_layer(pya.LayerInfo(1, 0))
    l2 = layout.insert_layer(pya.LayerInfo(2, 0))

    for i in range(21):
        for j in range(21):
            box = pya.DBox(0, 0, 10, 10)
            box.move(15 * i, 15 * j)
            TOP.shapes(l1).insert(box)
    TOP.shapes(l2).insert(pya.DBox(0,0,500,500))

simple_create()
