''' Demonstrates a tracer program that reloads layout after every call to phidl.Device.add_ref (i.e. <<)

    This runs fine in klayout's GSI interpreter too
'''
try:
    import lyipc
except ImportError:
    print('Warning: lyipc is not installed on your PYTHONPATH.')
    print('Continuing with relative path for now...\n' + '-' * 50)
    import sys
    from os.path import join, dirname
    sys.path.append(join(dirname(__file__), '..', 'python'))


import lyipc.client.phidl as ipc
# from lyipc.client.phidl import trace_phidladd
import os
import time
import phidl


debug_file = os.path.realpath('debuglobal.gds')
ipc.load(debug_file)

def simple_create():
    D = phidl.Device()
    ipc.trace_phidladd(D, 'debuglobal.gds')

    l1 = phidl.Layer(1)
    for i in range(4):
        for j in range(4):
            box = phidl.geometry.rectangle(size=(10, 10), layer=l1)
            box.move((15 * i, 15 * j))
            D << box


simple_create()
