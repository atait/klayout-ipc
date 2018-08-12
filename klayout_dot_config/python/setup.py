from setuptools import setup, find_packages

def readme():
    with open('README.rst') as fx:
        return fx.read()

setup(name='lyipc',
      version='0.1.2',
      description='Inter-process communication for Klayout',
      long_description=readme(),
      author='Alex Tait',
      author_email='alexander.tait@nist.gov',
      license='MIT',
      packages=find_packages(),
      install_requires=[],
      )
