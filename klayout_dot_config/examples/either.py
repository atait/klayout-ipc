''' Test script with no dependencies on layout packages

    This should have the same behavior whether interpreted by klayout or python
'''

from os.path import join, dirname
import sys
sys.path.append(join(dirname(__file__), '..', 'python'))

import lyipc.client as ipc
import time, os

print('Sending ping')
ipc.send('ping')

print('Going to load gds now')
gdsname = os.path.realpath('box.gds')
ipc.load(gdsname)

print('Done')