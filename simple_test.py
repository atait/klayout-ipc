import lygadgets
lygadgets.patch_environment()

import lyipc
from lyipc.client.dependent import _get_write_method

# Test pya writables
import pya
layout = pya.Layout()
assert _get_write_method(layout) == layout.write
TOP = layout.create_cell('TOP')
assert _get_write_method(TOP) == TOP.write


# Test phidl writables
import phidl
box2 = phidl.geometry.rectangle((20, 20))
assert _get_write_method(box2) == box2.write_gds