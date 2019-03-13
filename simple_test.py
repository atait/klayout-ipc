import lygadgets
from lygadgets import any_write, any_read
lygadgets.patch_environment()
import os

def test_writes():
    # Test pya writables
    import pya
    layout = pya.Layout()
    any_write(layout, 'tempfile.gds')
    TOP = layout.create_cell('TOP')
    any_write(TOP, 'tempfile.gds')


    # Test phidl writables
    import phidl
    box2 = phidl.geometry.rectangle((20, 20))
    any_write(box2, 'tempfile.gds')
    os.remove('tempfile.gds')
