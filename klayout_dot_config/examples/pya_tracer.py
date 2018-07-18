''' Automatically launches a subprocess klayout and drops into debug shell
'''

import os
import time
import numpy as np
from functools import partial

import pya
import sys
import lyipc.client.pya as ipc

debug_file = os.path.realpath('debuglobal.gds')


def simple_create():
    layout = pya.Layout()
    ipc.trace_pyainsert(layout, debug_file, 0.02)
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
    ipc.trace_pyainsert(layout, debug_file, 1e-4)
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


tough_create()
