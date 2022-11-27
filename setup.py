from setuptools import setup
from MAVdataflash import __version__ as version

with open('requirements.txt') as req:
    install_requires = req.read()

setup(name='MAVdataflash',
    version=version,
    url='https://github.com/generalaeronautics/MAVdataflash',
    description='Read, analyze and visualize *.bin flight data logs recorded by ArduPilot',
    author='General Aeronautics',
    packages=['MAVdataflash'],
    include_package_data=True,
    install_requires=install_requires,
    python_requires='>=3.6',
    )