''' First start an application instance. Run the lyIPC.

    Then run this from command line with "klayout -b -r for_pya.py"
'''
import pya
# import klayout.db as pya
import lyipc.client.pya as ipc
import time
import os


gdsname = os.path.realpath('box.gds')

# Define layouts, layers, cell
layout = pya.Layout()
layout.dbu = 0.001
TOP = layout.create_cell('TOP')
l1 = layout.insert_layer(pya.LayerInfo(1, 0))

# Create and place a rectangle
box = pya.DBox(pya.DPoint(0, 0), pya.DPoint(20, 20))
TOP.shapes(l1).insert(box)

# Write and tell Klayout GUI to open the file
layout.write(gdsname)
ipc.load(gdsname)


# Changing the flow in a debugger and animation, sort of
for i in range(11):
    box2 = pya.DBox(pya.DPoint(2 * i, 2 * i), pya.DPoint(40, 40))

    if i == 7:
        import pdb; pdb.set_trace()
        # Path 1: let the debugger continue
        # Path 2: execute the following line in debugger, then continue
        # box2 = box2.move(40, 0)
    TOP.shapes(l1).insert(box2)
    layout.write(gdsname)
    ipc.reload()
    time.sleep(0.1)
