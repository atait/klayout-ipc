''' These are functions that are independent of the layout package '''
from __future__ import print_function
from . import send
from functools import lru_cache
import os


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
