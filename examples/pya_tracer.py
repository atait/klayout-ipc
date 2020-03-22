''' Automatically launches a subprocess klayout and drops into debug shell
'''

import os
import time
import numpy as np
import time

import pya
import sys
import lyipc.client.pya as ipc

debug_file = os.path.realpath('debuglobal.gds')

# Clear and open the file
if not os.path.isfile(debug_file):
    from lygadgets import any_write
    any_write(pya.Layout(), debug_file)
ipc.load(debug_file)


def simple_create(grids=4):
    t0 = time.time()
    layout = pya.Layout()
    ipc.trace_pyainsert(layout, debug_file)

    layout.dbu = 0.001
    TOP = layout.create_cell('TOP')
    l1 = layout.insert_layer(pya.LayerInfo(1, 0))

    for i in range(grids):
        for j in range(grids):
            box = pya.DBox(0, 0, 10, 10)
            box.move(15 * i, 15 * j)
            TOP.shapes(l1).insert(box)
    print(time.time() - t0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        simple_create()
    else:
        simple_create(int(sys.argv[1]))
