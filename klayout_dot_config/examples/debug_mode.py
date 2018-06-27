''' First start an application instance. Run the lyIPC.

    Then run this from command line with "klayout -b -r debug_mode.py"
'''
import pya
import lyipc.client as ipc
import time
import os


gdsname = os.path.realpath('box.gds')
layout = pya.Layout()
layout.dbu = 0.001
TOP = layout.create_cell('TOP')

l1 = layout.insert_layer(pya.LayerInfo(1, 0))

box = pya.DBox(pya.DPoint(0, 0), pya.DPoint(20, 20))
# box2 = box.dup()
# Cell.shapes is like a dictionary keyed by layer whose values are Shapes objects
TOP.shapes(l1).insert(box)
# TOP.shapes(l1).insert(box2)
# import pdb; pdb.set_trace()

layout.write(gdsname)
ipc.load(gdsname)

for i in range(10):
    box2 = pya.DBox(pya.DPoint(2 * i, 2 * i), pya.DPoint(40, 40))
    # if i == 4:
    #     import pdb; pdb.set_trace()
        # Path 1: let the debugger continue
        # Path 2: execute the following line in debugger
        # box2 = box2.move(40, 0)
    TOP.shapes(l1).insert(box2)
    layout.write(gdsname)
    ipc.reload()
    time.sleep(0.1)

# ipc.kill()

print('Exiting')