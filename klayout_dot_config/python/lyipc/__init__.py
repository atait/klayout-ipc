# import pya
PORT = 11078

def isGSI():
    try:
        import pya
        return True
    except ImportError:
        return False

def isGUI():
    import pya
    if isGSI() and pya.Application.instance().main_window() is not None:
        return True
    else:
        return False


# This package should be compatible with GUI/batch klayout/python clients/servers. Reporting is different for each
def quickmsg(msg):
    if isGUI():
        import pya
        pya.MessageBox.info('lyipc', msg, pya.MessageBox.Ok)
    else:
        print(' lyipc:', msg)