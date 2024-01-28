''' These are functions specific to pya
    There is not necessarily any similarity with implementation in other languages
    If pya not present, lygadgets will allow import but not use of these functions
'''
from __future__ import print_function
from lygadgets import pya

# Makes it so that only one import is needed: lyipc.client.pya will drop in for lyipc.client
from lyipc.client.general import view
from lyipc.client.dependent import klayout_quickplot

ignore_layers = []
def trace_pyainsert(layout, file):
    ''' Writes to file and loads in the remote instance whenever pya.Shapes.insert is called
        "layout" is what will be written to file and loaded there.

        Intercepts pya.Shapes.insert globally, not just for the argument "layout".
        This is because usually cells are generated before they are inserted into the layout,
        yet we would still like to be able to visualize their creation.

        Update: the cellview is switched to the one in which the shape is being drawn.
    '''
    # Intercept Shapes.insert
    pya.Shapes.old_insert = pya.Shapes.insert
    def new_insert(self, *args, **kwargs):
        retval = pya.Shapes.old_insert(self, *args, **kwargs)
        if hasattr(self, 'traced_cell'):
            klayout_quickplot(layout, file, fresh=False)
            view(self.traced_cell)
        return retval
    pya.Shapes.insert = new_insert

    # Intercept Cell.shapes
    pya.Cell.old_shapes = pya.Cell.shapes
    def new_shapes(self, *args, **kwargs):
        theshape = pya.Cell.old_shapes(self, *args, **kwargs)
        if args[0] not in ignore_layers:
            theshape.traced_cell = self.name
        return theshape
    pya.Cell.shapes = new_shapes


def trace_SiEPICplacecell(layout, file, write_load_delay=0.01):
    ''' Uses trace_pyainsert to intercept geometry creation, and also makes Pcells
        place within the parent cell before being created.
        Normally, pcells are created before they are placed.

        TESTED to be NOT WORKING
    '''
    trace_pyainsert(layout, file, write_load_delay)
    import SiEPIC.utils.pcells as kpc
    kpc.KLayoutPCell.old_place_cell = kpc.KLayoutPCell.place_cell
    def new_place_cell(self, parent_cell, origin, params=None, relative_to=None, transform_into=False):
        layout = parent_cell.layout()
        # Build it to figure out the ports. Don't trace that
        # untrace_pyainsert()
        pcell, ports = self.pcell(layout, params=params)
        # layout.delete_cell(pcell.cell_index())
        # Place an empty cell
        new_cell = layout.create_cell(self.name)
        retval = kpc.place_cell(parent_cell, new_cell, ports, origin, relative_to=relative_to, transform_into=transform_into)
        # Build it again, this time in place. Trace it as it builds
        # trace_pyainsert(layout, file, write_load_delay)
        self.pcell(layout, cell=new_cell, params=params)
        return retval
    kpc.KLayoutPCell.place_cell = new_place_cell
