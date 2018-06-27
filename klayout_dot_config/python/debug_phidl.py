''' First start an application instance. Run the lyIPC.

    Then run this from command line with "klayout -b -r debug_mode.py"
'''
import lyipc.client as ipc
# import pdb; pdb.set_trace()
# ipc.send()
import os
import time

import phidl
# from phidl import quickplot2 as qp

gdsname = os.path.realpath('box.gds')

TOP = phidl.Device('TOP')
somelayer = phidl.Layer(1)
box = phidl.geometry.rectangle(size=(20, 20), layer=somelayer)
box_ref1 = TOP.add_ref(box)
box_ref2 = TOP.add_ref(box)

TOP.write_gds(gdsname)
ipc.load(gdsname)

which_way = 1
for i in range(10):
    box_ref2.move((10, 10 * which_way))
    if i == 4:
        import pdb; pdb.set_trace()
        # Path 1: let the debugger continue
        # Path 2: execute the following line in debugger
        # which_way *= -1
    TOP.write_gds(gdsname)
    ipc.load(gdsname)
    time.sleep(0.2)



# qp(TOP) # quickplot it!
# import pdb; pdb.set_trace()

print('Exiting')