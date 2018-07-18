''' These are functions that are independent of the layout package '''
from __future__ import print_function
from . import send
from functools import lru_cache
import os
import time
from functools import wraps


def reload():
    send('reload view')


fast_realpath = lru_cache(maxsize=4)(os.path.realpath)  # Since the argument is going to be the same every time
def load(filename):
    filename = fast_realpath(filename)
    # TODO: use a temporary file
    send(f'load {filename}')


def kill():
    send('kill')


def diff(file1, file2):
    pass  # TODO


#: Mapping of writable base classes used by this program to the name of their write methods.
#: This is set at import time by whichever non-general module that is imported.
#: pya.Cell and pya.Layout have 'write'; phidl.Device and gdspy.Cell have 'write_gds'
write_methods = dict()


def klayout_quickplot(writable_obj, file, fresh=False, write_load_delay=0.01):
    ''' Does the write, wait, and load all in one.
        The fresh argument determines whether to load (True) or reload (False)

        The write function used is class and language-specific,
        determined by the contents of ``write_methods``.
    '''
    # Does the object inherit from any classes in the write methods
    for parent_class in type(writable_obj).mro():
        if parent_class in write_methods.keys():
            base_class = parent_class
            break
    else:
        raise KeyError(type(writable_obj).__name__ + ': write_methods not declared for this class')
    # Get the write method that is bound to this object and call it
    method_name = write_methods[base_class]
    bound_write = getattr(writable_obj, method_name)
    bound_write(file)
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
