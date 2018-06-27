''' This should run and have the same behavior whether interpreted by klayout or python
'''

# import pdb; pdb.set_trace()
import lyipc.client as ipc
import time, os

print('Sending message')
ipc.send('ping')

print('Going to load gds now')
gdsname = os.path.realpath('box.gds')
ipc.load(gdsname)

print('Exiting')