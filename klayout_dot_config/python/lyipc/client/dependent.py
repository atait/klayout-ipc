''' These depend on the language being used but have very similar implementation across languages.
    For example, every one has some way to write layout objects to a gds file.
'''
from __future__ import print_function
import os
import time
from functools import wraps
from .general import load, reload


global __unbound_method_names
__unbound_method_names = dict()  # this is a cache to avoid lots of importing
def _get_write_method(writable_obj):
    ''' This function resolves write methods for cell/layout objects across languages.

        If the class is a phidl.Device, we will dynamically import gdspy, then check if it is a subclass of gdspy.Cell.
        It is, so then then we return the "write_gds" method which is bound to ``writable_obj``.

        Args:
            (object): layout data object that can be written, typically Cell or Layout or Device

        Returns:
            (func): bound method corresponding to a method that produces a file output (often GDS)
    '''
    global __unbound_method_names

    if type(writable_obj) not in __unbound_method_names.keys():
        # It has not been added to the cache yet. Search for the method in the library.
        try:
            import gdspy  # phidl and others are based on gdspy, so this covers them
            if isinstance(writable_obj, gdspy.Cell):
                __unbound_method_names[type(writable_obj)] = 'write_gds'
        except ImportError:
            pass

        try:
            import pya
            if isinstance(writable_obj, (pya.Cell, pya.Layout)):
                __unbound_method_names[type(writable_obj)] = 'write'
        except ImportError:
            pass

    found_meth_name = __unbound_method_names[type(writable_obj)]
    return getattr(writable_obj, found_meth_name)



def klayout_quickplot(writable_obj, file, fresh=False, write_load_delay=0.01, write_kwargs=None):
    ''' Does the write, wait, and load all in one.
        The fresh argument determines whether to load (True) or reload (False)

        The write function used is class and language-specific,
        so the ``writable_obj`` is handled according to the _get_write_method function
    '''
    if write_kwargs is None:
        write_kwargs = {}
    _get_write_method(writable_obj)(file, **write_kwargs)
    # Wait for file to finish writing
    time.sleep(write_load_delay)
    # Tell remote klayout GUI to load/reload it
    if fresh:
        load(file)
    else:
        reload()


def generate_display_function(default_writable_obj, default_file):
    ''' A quick way to configure quickplotter into a brief command

        Usage::
            TOP = Layout()
            kqp = make_display_function(TOP, 'debugging.gds')
            ...
            kqp()
    '''
    default_file = os.path.realpath(default_file)
    @wraps(klayout_quickplot)
    def k_quick(writable_obj=default_writable_obj, file=default_file, **kwargs):
        klayout_quickplot(writable_obj, file, **kwargs)
    return k_quick