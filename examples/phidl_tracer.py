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
import os
import time
import phidl


debug_file = os.path.realpath('debuglobal.gds')

# Clear and open the file
if not os.path.isfile(debug_file):
    from lygadgets import any_write
    any_write(phidl.Device(), debug_file)
ipc.load(debug_file)


def simple_create(grids=4):
    t0 = time.time()
    D = phidl.Device()
    ipc.trace_phidladd(D, 'debuglobal.gds')

    l1 = phidl.Layer(1)
    for i in range(grids):
        for j in range(grids):
            box = phidl.geometry.rectangle(size=(10, 10), layer=l1)
            box.move((15 * i, 15 * j))
            D << box
    print(time.time() - t0)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        simple_create()
    else:
        simple_create(int(sys.argv[1]))
