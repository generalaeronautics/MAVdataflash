from setuptools import setup

with open('requirements.txt') as req:
    install_requires = req.read()

setup(name='MAVdataflash',
    version='2.2',    
    description='Read, analyze and visualize *.bin flight data logs recorded by ArduPilot',
    author='General Aeronautics',
    packages=['MAVdataflash'],
    install_requires=install_requires,
    python_requires='>=3.6',
    include_package_data=True
    )