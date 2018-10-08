from setuptools import setup
import os


def my_postinstall():
    try:
        from lygadgets import post_install_factory
    except (ImportError, ModuleNotFoundError):
        print('\033[95mlygadgets not found, so klayout package not linked.')
        print('Please download it in the klayout Package Manager\033[0m')
        return dict()
    else:
        my_config_dir = os.path.realpath(os.path.join('..', '..', 'klayout_dot_config'))
        return {'install': post_install_factory(my_config_dir)}


def readme():
    with open('README.rst') as fx:
        return fx.read()


setup(name='lyipc',
      version='0.1.7',
      description='Inter-process communication for Klayout',
      long_description=readme(),
      author='Alex Tait',
      author_email='alexander.tait@nist.gov',
      license='MIT',
      packages=['lyipc', 'lyipc/client'],
      install_requires=[],
      cmdclass=my_postinstall(),
      )
