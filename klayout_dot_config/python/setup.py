from setuptools import setup, find_packages
from setuptools.command.install import install

def is_windows():
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return False
    elif platform == "darwin":
        return False
    elif platform == "win32":
        return True
    else:
        raise ValueError('Unrecognized operating system: {}'.format(platform))


import os
def link_to_salt():
    user_home = os.path.expanduser('~')
    if is_windows():
        klayout_config_dir = os.path.join(user_home, 'KLayout')
    else:
        klayout_config_dir = os.path.join(user_home, '.klayout')
    if not os.path.exists(klayout_config_dir):
        raise FileNotFoundError('The KLayout config directory was not found. KLayout might not be installed.')
    salt_dir = os.path.join(klayout_config_dir, 'salt')
    if not os.path.exists(salt_dir):
        os.mkdir(salt_dir)
    salt_link = os.path.join(salt_dir, 'klayout_ipc')

    lyipc_config = os.path.realpath(os.path.join('..', '..', 'klayout_dot_config'))

    if not is_windows():
        os.symlink(lyipc_config, salt_link)  # so easy. Thanks UNIX
    else:
        try:
            os.symlink(lyipc_config, salt_link)
            return
        except AttributeError:
            pass
        import subprocess
        try:
            retval = subprocess.call(['ln', '-s', lyipc_config, salt_link])
            assert retval == 0
            return
        except (subprocess.CalledProcessError, WindowsError, AssertionError):
            pass
        try:
            windows_symlink_override(lyipc_config, salt_link)
            return
        except WindowsError:
            pass
        raise WindowsError('Failed to find a way to link to a file in windows')


def windows_symlink_override(source, link_name):
    ''' Creates a symbolic link pointing to source named link_name.
        From https://stackoverflow.com/questions/1447575/symlinks-on-windows
    '''
    import ctypes
    csl = ctypes.windll.kernel32.CreateSymbolicLinkW
    csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
    csl.restype = ctypes.c_ubyte
    flags = 0
    if source is not None and os.path.isdir(source):
        flags = 1
    if csl(link_name, source, flags) == 0:
        raise ctypes.WinError()


def readme():
    with open('README.rst') as fx:
        return fx.read()


class PostInstall(install):
    def run(self):
        install.run(self)
        try:
            link_to_salt()
        except Exception as err:
            print('Autoinstall into klayout salt failed with the following')
            print(err)
            print('\nYou must perform a manual install as described in the README.')


setup(name='lyipc',
      version='0.1.7',
      description='Inter-process communication for Klayout',
      long_description=readme(),
      author='Alex Tait',
      author_email='alexander.tait@nist.gov',
      license='MIT',
      packages=find_packages(),
      install_requires=[],
      cmdclass={'install': PostInstall},
      )
