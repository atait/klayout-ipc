# import pya
PORT = 11031


# This package should be compatible with GUI/batch klayout/python clients/servers. Reporting is different.
def quickmsg(msg):
    try:
        import pya
    except ImportError:
        print(' lyipc:', msg)
        return
    if pya.Application.instance().main_window() is not None:
        pya.MessageBox.info('lyipc', msg, pya.MessageBox.Ok)
    else:
        print(' lyipc:', msg)