from setuptools import setup
import os


def readme():
    with open('README.md') as fx:
        return fx.read()


setup(name='lyipc',
      version='0.2.14',
      description='Inter-process communication for Klayout',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='https://github.com/atait/klayout-ipc',
      author='Alex Tait',
      author_email='alexander.tait@nist.gov',
      license='MIT',
      packages=['lyipc', 'lyipc/client'],
      install_requires=['lygadgets>=0.1.19'],
      package_data={'': ['*.lym']},
      include_package_data=True,
      entry_points={'console_scripts': [
        'lyipc_reload=lyipc.client.command_line:cm_reload',
      ]},
      )
