import os
import shutil
import socket
import subprocess

target_host = None
def set_target_hostname(hostalias, persist=False):
    ''' if it is a remote, you must have already set up an RSA key and alias in your ~/.ssh/config file.
        On that computer, this computer's RSA key needs to be in ~/.ssh/authorized_keys.
        Instructions: https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2

        Example: atait@tait-computer

        persist means through the terminal session. It sets environment variable
        not persist means through this python session. It doesn't last as long. It takes precedence.
    '''
    global target_host
    if hostalias == 'localhost':
        hostalias = socket.gethostbyname(hostalias)
    if persist:
        os.environ['LYIPCTARGET'] = target_host
    else:
        target_host = hostalias


def get_target_hostname(incl_user=True):
    ''' Target host information

        incl_user=True will give you something like 'atait@tait-computer'.
        Use this for rsync.

        incl_user=False will give 'tait-computer'
        Use this for ssh.
    '''
    if target_host is not None:
        host = target_host
    else:
        try:
            host = os.environ['LYIPCTARGET']
        except KeyError:
            return socket.gethostbyname('localhost')
    if not incl_user:
        host = host.split('@')[-1]
    return host


# set_target_hostname('localhost')


def is_host_remote():
    return get_target_hostname(incl_user=False) != socket.gethostbyname('localhost')


def call_report(command, verbose=True):
    if verbose:
        myprint = print
    else:
        myprint = lambda *args: None
    myprint('\n[[' + ' '.join(command) + ']]\n')
    try:
        ret = subprocess.check_output(command).decode()
    except subprocess.CalledProcessError as err:
        myprint(err.output.decode())
        raise
    else:
        myprint(ret)
        return ret


def call_ssh(command, verbose=True):
    # command[0] = '"' + command[0]
    # command[-1] = command[-1] + '"'
    ssh_command = ['ssh', '-qt', get_target_hostname()]  # q silences welcome banner, t retains text coloring
    ssh_command += command
    return call_report(ssh_command, verbose=verbose)


def host_HOME():
    if not is_host_remote():
        return os.environ['HOME']
    else:
        return call_ssh(['echo', '$HOME']).strip()


def rsync(source, dest, verbose=True):
    rsync_call = ['rsync', '-avzh']
    rsync_call += [source, dest]
    call_report(rsync_call, verbose=verbose)


def ship_file(local_file, target_host=None):
    ''' returns the name of the remote file
        This currently assumes that the host has the same operating system separator as this one (e.g. "/")
    '''
    if not is_host_remote() and target_host is None:
        return local_file
    if target_host is None:
        target_host = get_target_hostname()
    # where are we going to put it
    local_file = os.path.realpath(local_file)
    # rel_filepath = os.sep.join(local_file.split(os.sep)[-3:-1])  # pick off a few directories to avoid name clashes
    rel_filepath = ''
    remote_path = os.path.join('tmp_lypic', rel_filepath)
    remote_file = os.path.join(host_HOME(), remote_path, os.path.basename(local_file))
    rsync(local_file, target_host + ':' + remote_path)
    return remote_file


def retrieve_file(remote_file, target_host=None):
    ''' As of now, you must specify the full path, except ~ is allowed if the remote computer is UNIX.
        returns the path to the local file, which is placed in the current directory by default.
        target_host has the format of atait@tait-computer. Default is the persistent setting.
    '''
    if not is_host_remote() and target_host is None:
        return remote_file
    if target_host is None:
        target_host = get_target_hostname()
    local_file = os.path.basename(remote_file)
    rsync(target_host + ':' + remote_file, local_file)
    return local_file
