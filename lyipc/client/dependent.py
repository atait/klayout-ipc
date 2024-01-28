''' These depend on the language being used but have very similar implementation across languages.
    For example, every one has some way to write layout objects to a gds file.
'''
from __future__ import print_function
import os
import time
from functools import wraps
from lyipc.client.general import load, reload, ServerSideError
from lyipc.client.remotehost import is_host_remote

from lygadgets import any_write


def safe_write(writable_obj, filename, write_kwargs=None):
    ''' Writes a temporary file then waits until it finishes writing before moving to the desired filename
    '''
    dirname, basename = os.path.split(filename)
    temp_filename = os.path.join(dirname, '~.' + basename)
    if write_kwargs is None:
        write_kwargs = dict()
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
    try:
        any_write(writable_obj, temp_filename, **write_kwargs)
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
    # reload does not work remote
    if is_host_remote():
        fresh = True
    # Tell remote klayout GUI to load/reload it
    if fresh:
        load(filename)
    else:
        reload(filename)


def generate_display_function(default_writable_obj, default_filename):
    ''' A quick way to configure quickplotter into a brief command

        Usage::
            TOP = Layout()
            kqp = make_display_function(TOP, 'debugging.gds')
            ...
            kqp(...)
    '''
    default_filename = os.path.realpath(default_filename)
    @wraps(klayout_quickplot)
    def k_quick(writable_obj=default_writable_obj, filename=default_filename, **kwargs):
        klayout_quickplot(writable_obj, filename, **kwargs)
    return k_quick
