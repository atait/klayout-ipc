''' All of lyipc is visible within klayout's interpreter namespace,
    but it is not on the system python path.
    In order for an external client to use it, lyipc should be installed on the path.

    Do that with "python setup.py install".

    Elsewhere, you can now "import lyipc.client"
'''
from setuptools import setup

def readme():
    with open('README.rst') as fx:
        return fx.read()

setup(name='lyipc',
      version='0.0.1',
      description='Inter-process communication for Klayout',
      long_description=readme(),
      author='Alex Tait',
      author_email='alexander.tait@nist.gov',
      license='MIT',
      packages=['lyipc'],
      install_requires=[],
      )