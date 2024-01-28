import argparse
import lyipc
from lyipc.client.general import load, reload

parser = argparse.ArgumentParser(description="lyipc load/reload CLI")
parser.add_argument('-f', '--fresh', action='store_true',
                    help='force replacement of current window. KLayout will ask if changes need to be saved')
parser.add_argument('-a', '--address', type=str, nargs='?', const='-1', default=None,
                    help='address of target hostname')
parser.add_argument('-p', '--port', type=int, nargs='?', const=-1, default=None,
                    help='target port')
parser.add_argument('-v', '--version', action='version', version=f'%(prog)s v{lyipc.__version__}')
parser.add_argument('filename', type=str, nargs='?', default=None,
                    help='The GDS or OAS file')

def cm_reload():
    args = parser.parse_args()
    if args.address is not None:
        if args.address == '-1':
            raise ValueError('-a, --address must be given an argument')
        set_target_hostname(args.address)
    if args.port is not None:
        if args.port == -1:
            raise ValueError('-p, --port must be given an argument')
        lyipc.PORT = args.port
    if args.fresh:
        if args.filename is None:
            raise ValueError('When --fresh is set, a filename must be provided')
        load(args.filename)
    else:
        reload(args.filename)
