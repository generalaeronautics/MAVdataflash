from setuptools import setup

setup(name='MAVdataflash',
    version='2.0',    
    description='Read, analyze and visualize *.bin flight data logs recorded by ArduPilot',
    author='General Aeronautics',
    packages=['MAVdataflash'],
    install_requires=['pymavlink>=2.4.35',
		      'polars>=0.14.15',
		      'pyarrow',
 		      'pandas',
		      'matplotlib'               
                      ],
    python_requires='>=3.6',
    include_package_data=True
    )