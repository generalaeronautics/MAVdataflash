# MAVdataflash
Read, analyze and visualize *.bin flight data logs recorded by ArduPilot

## Usage
```python
from MAVdataflash import DataFlash
```
```python
# Create a new instance with DataFlash class
analysis = DataFlash("flight_data.bin")
```

```python
# Return data in pandas dataframe
analysis.GetData('GPS')

# Return data in polars dataframe
analysis.GetData('GPS', in_polars=True)
```

```python
# Plot any Parameter and Subparameter VS Time
analysis.Plot('GPS', 'Alt')

# Plot with instance, if parameter data type has more than 1 instance
analysis.Plot('IMU', 'GyrX', instance=1)
```

```python
# Return the pandas dataframe of EV(Events) data type with Message
analysis.GetEvents()

# Return in polars dataframe
analysis.GetEvents(in_polars=True)
```

```python
# Return the list of Subparameter(Columns) of the Parameter data type
analysis.GetColumns('GPS')
```

```python
# Return True if Parameter data type is plottable otherwise return as False
analysis.isPlotable('GPS')
analysis.isPlotable('GPS', column='Alt')
```

## Installation
MAVdataflash is not yet in PyPI, so you can install directly from the source code:

    $ pip install https://github.com/generalaeronautics/MAVdataflash/archive/refs/heads/latest.zip

If you have git installed, you can also try:

    $ pip install git+https://github.com/generalaeronautics/MAVdataflash.git

You can also install by cloning or downloading the repo:

    $ git clone https://github.com/generalaeronautics/MAVdataflash
    $ cd MAVdataflash
    $ pip install .

If you get any installation or compilation errors, make sure you have the latest pip and setuptools::

    $ pip install --upgrade pip setuptools

## Requirements
* pymavlink
* polars
* pandas
* pyarrow
* matplotlib
