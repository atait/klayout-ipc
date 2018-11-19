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
    '''
    global target_host
    if hostalias == 'localhost':
        hostalias = socket.gethostbyname(hostalias)
    target_host = hostalias
    if persist:
        os.environ['LYIPCTARGET'] = target_host


def get_target_hostname(incl_user=True):
    try:
        host = os.environ['LYIPCTARGET']
    except KeyError:
        host = target_host
    if not incl_user:
        host = host.split('@')[-1]
    return host


set_target_hostname('localhost')


def is_host_remote():
    return get_target_hostname() != socket.gethostbyname('localhost')


def call_report(command, verbose=True):
    if verbose:
        print = lambda *args: None
    print('\n[[' + ' '.join(command) + ']]\n')
    try:
        ret = subprocess.check_output(command).decode()
    except subprocess.CalledProcessError as err:
        print(err.output.decode())
        raise
    else:
        print(ret)
        return ret


def call_ssh(command):
    # command[0] = '"' + command[0]
    # command[-1] = command[-1] + '"'
    ssh_command = ['ssh', '-t', get_target_hostname()] + command
    return call_report(ssh_command)


def host_HOME():
    if not is_host_remote():
        return os.environ['HOME']
    else:
        return call_ssh(['echo', '$HOME']).strip()


def rsync(source, dest, verbose=True):
    rsync_call = ['rsync', '-avzh']
    rsync_call += [source, dest]
    call_report(rsync_call, verbose=verbose)


def ship_file(local_file):
    ''' returns the name of the remote file
        This currently assumes that the host has the same operating system separator as this one (e.g. "/")
    '''
    if not is_host_remote():
        return local_file
    # where are we going to put it
    local_file = os.path.realpath(local_file)
    # rel_filepath = os.sep.join(local_file.split(os.sep)[-3:-1])  # pick off a few directories to avoid name clashes
    rel_filepath = ''
    remote_path = os.path.join('tmp_lypic', rel_filepath)
    remote_file = os.path.join(remote_path, os.path.basename(local_file))
    rsync(local_file, get_target_hostname() + ':' + remote_path)
    return os.path.join(host_HOME(), remote_file)
