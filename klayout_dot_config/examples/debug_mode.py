''' First start an application instance. Run the lyIPC.

    Then run this from command line with "klayout -b -r debug_mode.py"
'''
import pya
import lyipc
from lyipc.client import remotewrite, remoteload, send
import time
import os

# gdsname = os.path.realpath('box.gds')
# layout = pya.Layout()
# layout.dbu = 0.001
# TOP = layout.create_cell('TOP')

# l1 = layout.insert_layer(pya.LayerInfo(1, 0))

# box = pya.DBox(pya.DPoint(0, 0), pya.DPoint(20, 20))
# TOP.shapes(l1).insert(box)

# layout.write(gdsname)
send('Preparing to send')
# time.sleep(2)

# remoteload(gdsname)

# print('Sleeping')
# time.sleep(3)

# box2 = pya.DBox(pya.DPoint(20, 20), pya.DPoint(40, 40))
# TOP.shapes(l1).insert(box2)

# layout.write(gdsname)
# remoteload(gdsname)

# print('Exiting')