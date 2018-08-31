KLayout inter-process communication (lyipc)
===========================================

This is brief documentation. To see the full project and documentation, go to https://github.com/atait/klayout-ipc.

Setup
***************************************
If you are a user, do::

    pip install lyipc

If you are installing from source and/or developing, you are probably not reading this on PyPI but rather on github. Anyways, the best way is to install using the local setup.py formulation.::

    pip install -e klayout-ipc/klayout_dot_config/python

Usage
*****
After setup, any python program can now::

    import lyipc.client as ipc
    ipc.load('mygds.gds')

assuming that there exists an instance of KLayout running the server on a visible port.
