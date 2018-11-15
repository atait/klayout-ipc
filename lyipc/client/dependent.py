''' These depend on the language being used but have very similar implementation across languages.
    For example, every one has some way to write layout objects to a gds file.
'''
from __future__ import print_function
import os
import time
from functools import wraps
from lyipc.client.general import load, reload


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


def safe_write(writable_obj, filename, write_kwargs=None):
    ''' Writes a temporary file then waits until it finishes writing before moving to the desired filename
    '''
    write_func = _get_write_method(writable_obj)
    dirname, basename = os.path.split(filename)
    temp_filename = os.path.join(dirname, '~.' + basename)
    if write_kwargs is None:
        write_kwargs = dict()
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
    try:
        write_func(temp_filename, **write_kwargs)
        os.rename(temp_filename, filename)
    except Exception as err:
        try:
            os.remove(temp_filename)
        except FileNotFoundError:
            pass
        raise err


def klayout_quickplot(writable_obj, filename, fresh=False, write_kwargs=None):
    ''' Does the write, wait, and load all in one.

        The write function used is class and language-specific,
        so the ``writable_obj`` is handled according to the _get_write_method function

        Args:
            writable_obj (object): some object that has a resolvable write GDS method (gdspy.Cell, phidl.Device, pya.Cell, pya.Layout)
            filename (str): file to write to
            fresh (bool): determines whether to load (True) or reload (False)
            write_kwargs (dict): kwargs that will be passed to the write function
    '''
    # Write and wait for filename to finish writing
    safe_write(writable_obj, filename, write_kwargs)
    # Tell remote klayout GUI to load/reload it
    if fresh:
        load(filename)
    else:
        reload()


def generate_display_function(default_writable_obj, default_filename):
    ''' A quick way to configure quickplotter into a brief command

        Usage::
            TOP = Layout()
            kqp = make_display_function(TOP, 'debugging.gds')
            ...
            kqp()
    '''
    default_filename = os.path.realpath(default_filename)
    @wraps(klayout_quickplot)
    def k_quick(writable_obj=default_writable_obj, filename=default_filename, **kwargs):
        klayout_quickplot(writable_obj, filename, **kwargs)
    return k_quick