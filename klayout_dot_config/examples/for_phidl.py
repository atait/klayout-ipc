''' Illustrates debugging non-Klayout programs

    First start a klayout application instance. Run the lyIPC.

    Then run this from command line with "python debug_phidl.py"

    Note that klayout can also run this file just fine.
'''
from os.path import join, dirname
import sys
sys.path.append(join(dirname(__file__), '..', 'python'))

import lyipc.client as ipc
import os
import time
import phidl


gdsname = os.path.realpath('box.gds')

# Define layouts, layers, cell
TOP = phidl.Device('TOP')
somelayer = phidl.Layer(1)

# Create and place a rectangle
box = phidl.geometry.rectangle(size=(20, 20), layer=somelayer)
box_ref = TOP.add_ref(box)

# Write and tell Klayout GUI to open the file
TOP.write_gds(gdsname)
ipc.load(gdsname)

for i in range(11):
    box2 = phidl.geometry.rectangle(size=(40 - 2 * i, 40 - 2 * i), layer=somelayer)
    box2.ymax = 40
    box2.xmax = 40

    if i == 7:
        import pdb; pdb.set_trace()
        # Path 1: let the debugger continue
        # Path 2: execute the following line in debugger
        # box2.move((40, 0))
    TOP.add_ref(box2)
    TOP.write_gds(gdsname)
    ipc.load(gdsname)
    time.sleep(0.2)
