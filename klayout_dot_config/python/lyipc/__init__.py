# import pya
PORT = 11078

def isGSI():
    ''' Detect whether we are in klayout's generic scripting interface
        Since pya cannot be imported from outside, try that.
    '''
    try:
        import pya
        return True
    except ImportError:
        return False

def isGUI():
    ''' Klayout can run as a window or in batch mode on command line
    '''
    if isGSI():
        import pya
        if pya.Application.instance().main_window() is not None:
            return True
    return False


def quickmsg(msg):
    if isGUI():
        import pya
        # pya.MessageBox.info('lyipc', msg, pya.MessageBox.Ok)
        pya.Application.instance().main_window().message(f'lyipc: {msg}', 2000)
    else:
        print(' lyipc:', msg)