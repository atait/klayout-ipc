from setuptools import setup
import os


def readme():
    with open('README.md') as fx:
        return fx.read()


setup(name='lyipc',
      version='0.2.5',
      description='Inter-process communication for Klayout',
      long_description=readme(),
      author='Alex Tait',
      author_email='alexander.tait@nist.gov',
      license='MIT',
      packages=['lyipc', 'lyipc/client'],
      install_requires=['lygadgets>=0.1.7'],
      package_data={'': ['*.lym']},
      include_package_data=True,
      cmdclass={},
      )
