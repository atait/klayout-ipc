''' Debugging with klayout's pya program

    First start an application instance. Run the lyIPC.

    Then run this from command line with "klayout -b -r for_pya.py"
'''
import pya
# import klayout.db as pya
import lyipc.client.pya as ipc
import os
import time

# Define layouts, layers, cell
layout = pya.Layout()
layout.dbu = 0.001
TOP = layout.create_cell('TOP')
l1 = layout.insert_layer(pya.LayerInfo(1, 0))


### Basic lyipc usage ###

gdsname = os.path.realpath('box.gds')

# Create and place a rectangle
box = pya.DBox(pya.DPoint(0, 0), pya.DPoint(20, 20))
TOP.shapes(l1).insert(box)

# Write and tell Klayout GUI to open the file
layout.write(gdsname)
ipc.load(gdsname)


### The debug workflow ###

kqp = ipc.generate_display_function(TOP, 'box.gds')

origin = pya.DPoint(0, 0)
turn = 0
for i in range(19):
    if i == 5:
        import pdb; pdb.set_trace()
        # Path 1: let the debugger continue
        # Path 2: execute "turn = 20" in debugger, then continue

    width = 40 - 2 * i
    box2 = pya.DBox(0, 0, width, width)
    box2 = box2.move(pya.DVector(origin))
    TOP.shapes(l1).insert(box2)
    origin = box2.p2 + pya.DVector(-turn, 0)

    kqp(fresh=True)
