from setuptools import setup
import os


try:
    from lygadgets import postinstall_lypackage
except (ImportError, ModuleNotFoundError):
    print('\033[95mlygadgets not found, so klayout package not linked.')
    print('Please download it in the klayout Package Manager\033[0m')
    my_postinstall = dict()
else:
    setup_dir = os.path.dirname(os.path.realpath(__file__))
    lypackage_dir = os.path.dirname(setup_dir)
    my_postinstall = {'install': postinstall_lypackage(lypackage_dir)}


def readme():
    with open('README.rst') as fx:
        return fx.read()


setup(name='lyipc',
      version='0.1.8',
      description='Inter-process communication for Klayout',
      long_description=readme(),
      author='Alex Tait',
      author_email='alexander.tait@nist.gov',
      license='MIT',
      packages=['lyipc', 'lyipc/client'],
      install_requires=[],
      cmdclass=my_postinstall,
      )
