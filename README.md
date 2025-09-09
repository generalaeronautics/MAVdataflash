# MAVdataflash
Read, analyze and visualize *.bin flight data logs recorded by ArduPilot

## Installation
#### Installing via [PyPI](https://pypi.org/project/MAVdataflash/)
Install the latest version with:
```
$ pip install --upgrade mavdataflash
```
#### Installing via [GitHub](https://github.com/generalaeronautics/MAVdataflash)
Install with source code,
```
$ git clone https://github.com/generalaeronautics/MAVdataflash
$ cd MAVdataflash
$ python -m build
$ pip install dist/*.whl
```
If you get any installation or compilation errors, make sure installed `build`:
```
$ pip install build setuptools wheel
```

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
analysis.GetData('IMU')

# Return data of specific instance in pandas dataframe
analysis.GetData('IMU', instance=1)

# Return data in polars dataframe
analysis.GetData('IMU', in_polars=True)
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
# Return the pandas dataframe of MODE(Modes) data type with Message
analysis.GetModes()

# Return in polars dataframe
analysis.GetModes(in_polars=True)
```

```python
# Return the pandas dataframe of PARM(Commands) with Values
analysis.GetPARAMS()

# Return Params with Date and Time included in dataframe
analysis.GetPARAMS(with_datetime=True)

# Return Params in dictionary data type
analysis.GetPARAMS(in_dict=True)

# Return in polars dataframe
analysis.GetPARAMS(in_polars=True)
```

```python
# Return PARM(Command) with Value
analysis.GetPARAM('EK3_IMU_MASK')
```

```python
# Return the list of Subparameter(Columns) of the Parameter data type
analysis.GetColumns('GPS')
```