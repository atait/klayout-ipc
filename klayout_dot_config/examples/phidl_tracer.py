''' Automatically launches a subprocess klayout and drops into debug shell
'''
from os.path import join, dirname
import sys

import lyipc.client.phidl as ipc
import os
import time
import phidl


debug_file = os.path.realpath('debuglobal.gds')

def simple_create():
    D = phidl.Device()
    ipc.trace_phidladd(D, debug_file, 0.02)
    l1 = phidl.Layer(1)
    for i in range(4):
        for j in range(4):
            box = phidl.geometry.rectangle(size=(10, 10), layer=l1)
            box.move((15 * i, 15 * j))
            D << box


simple_create()
