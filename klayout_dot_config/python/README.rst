KLayout inter-process communication (lyipc)
===========================================

This is brief documentation for the client side of the package. To see the full project and documentation, go to https://github.com/atait/klayout-ipc.

Setup
***************************************
The lyipc package is visible within klayout's interpreter namespace, but it is not on the system python path. In order for an external python-based program to use it, lyipc must be installed on the python path.

This is done in the klayout_dot_config/python directory with::

    python setup.py install

Usage
*****
After setup, any python program can now::

    import lyipc.client as ipc
    ipc.load('mygds.gds')

assuming that there exists an instance of KLayout running the server on a visible port.
