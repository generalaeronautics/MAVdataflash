from setuptools import setup
from MAVdataflash.__version__ import __version__ as version

with open('requirements.txt') as req:
    install_requires = req.read()

setup(name='MAVdataflash',
    version=version,
    url='https://github.com/generalaeronautics/MAVdataflash',
    description='Read, analyze and visualize *.bin flight data logs recorded by ArduPilot',
    long_description=''.join(open('README.md', encoding='utf-8').readlines()),
    long_description_content_type='text/markdown',
    author='General Aeronautics',
    packages=['MAVdataflash'],
    include_package_data=True,
    install_requires=install_requires,
    python_requires='>=3.6',
    )