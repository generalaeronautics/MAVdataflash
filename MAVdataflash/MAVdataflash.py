import datetime
from pymavlink import DFReader as DF
import polars as pl
import matplotlib.pyplot as plt
from MAVdataflash.__version__ import __version__ as version
from MAVdataflash.DataFlashDict import _dtypes, _dunits, _event_id, _mode_id, _mode_reason

class DataFlash:
    
    DFdict = {}   # Dictionary of all dtypes
    DFunit = {}  # Dictionary for dtypes units
    
    def __init__(self, filename):
        self.filename = filename
        self.version = version # MAVdataflash version

        self.DFdecode = DF.DFReader_binary(filename)
        while 1:
            # extracting FMT and FMTU for initialize the dataframe 
            DFmsg = self.DFdecode.recv_match(type=['FMT', 'FMTU'])
            if DFmsg is None:
                self.DFdecode.rewind()
                break
            # convert DF msg to Dict
            DFdict = DFmsg.to_dict()
            if DFdict['mavpackettype'] == 'FMT':
                DFdict['Columns'] = DFdict['Columns'].split(',')
                DFdict['Columns'] = [col.strip() for col in DFdict['Columns']] # to remove leading and trailing spaces in the keys
                DFdict['Columns'].insert(0, "DateTime")
                DFdict['Format'] = list(DFdict['Format'])
                DFdict['Format'].insert(0, "DT")
                # Initializing DataFrame with FMT message 
                DFcolumns_init = [pl.Series(column, dtype= _dtypes[dtype]) for column, dtype in zip(DFdict['Columns'], DFdict['Format'])]
                self.DFdict[DFdict['Name']] = pl.DataFrame(DFcolumns_init)
            elif DFdict['mavpackettype'] == 'FMTU':
                DFdict['UnitIds'] = list(DFdict['UnitIds'])
                DFdict['UnitIds'].insert(0, "-")
                # Exctracting Units and mutliplier for columns
                self.DFunit[self.DFdecode.id_to_name[DFdict['FmtType']]] = {column: _dunits[unit] 
                        for column, unit in zip(self.DFdict[self.DFdecode.id_to_name[DFdict['FmtType']]].columns, DFdict['UnitIds'])}
                            
    def _extract(self, dtype):
        DFlist = []
        if self.DFdict[dtype].shape[0] == 0:
            while 1:
                # extract the data type
                DFmsg = self.DFdecode.recv_match(type=dtype)
                if DFmsg is None:
                    self.DFdecode.rewind()
                    break
                DFdict_t = DFmsg.to_dict()
                DFdict = {}
                for field in DFmsg._fieldnames:
                    DFdict[field.strip()] = DFdict_t[field] # to remove leading and trailing spaces in the keys
                if 'mavpackettype' in DFdict: del DFdict['mavpackettype']
                DFdict = {'DateTime': datetime.datetime.fromtimestamp(DFmsg._timestamp), **DFdict}
                # list append of DFmsg
                DFlist.append(DFdict)
            if len(DFlist) != 0:
                # updating dataframe from DF list
                Data = pl.DataFrame(DFlist)
                Data = Data.with_columns(pl.col("DateTime").dt.cast_time_unit("ms"))
                self.DFdict[dtype] = pl.concat([self.DFdict[dtype], Data], how='diagonal')
            else: return None
    
    # Return column name of Instance.
    def _getInstance(self, dtype):
        column = self.GetColumns(dtype)
        if ('Instance' in column) or ('I' in column):
            if 'Instance' in column:
                return 'Instance'
            else:
                return 'I'
        else: return None

    def GetColumns(self, dtype):
        # Return column list of data types
        return self.DFdict[dtype].columns

    # Function to check data type or Column is Plotable
    def isPlotable(self, dtype, column=None):
        if column == None:
            if 'TimeUS' not in self.DFdict[dtype].columns: return False
            else: return True
        else:
            if "TimeUS" not in self.DFdict[dtype].columns or pl.datatypes.Utf8 == self.DFdict[dtype][column].dtype: return False
            else: return True

    # Function to extract and get data 
    def GetData(self, dtype, instance=None, in_polars=False):
        self._extract(dtype)
        if instance != None:
            instance_column = self._getInstance(dtype)
            if instance_column != None:
                data = self.DFdict[dtype].filter(pl.col(instance_column) == instance)
            else:
                data = self.DFdict[dtype]
        else:
            data = self.DFdict[dtype]
        if in_polars == True: return data
        else: return data.to_pandas()

    # Function to plot the data
    def Plot(self, dtype, column, instance=None):
        if self.isPlotable(dtype, column=column) == True:
            self._extract(dtype)
            if instance == None:
                xaxis = (self.DFdict[dtype]['DateTime']).to_list()
                yaxis = (self.DFdict[dtype][column]).to_list()
            else:
                xaxis = (self.DFdict[dtype].filter(pl.col("I") == instance)['DateTime']).to_list()
                yaxis = (self.DFdict[dtype].filter(pl.col("I") == instance)[column]).to_list()
            
            plt.figure(f'{dtype} - {column}')
            plt.xlabel('Time')
            plt.ylabel(f'{column} ({self.DFunit[dtype][column]})')
            plt.plot(xaxis, yaxis)
            plt.show()
        else:
            print(f"{column} parameter is not suitable for Plotting!")
    
    # Function to return Events details
    def GetEvents(self, in_polars=False):
        self._extract('EV')
        Event = self.DFdict['EV'].clone()
        if Event.shape[0] != 0:
            Events_DF = Event.apply(lambda column: (column[1], _event_id[column[2]]))
            Events_DF = Events_DF.rename({"column_0": "TimeUS", "column_1": "Event"})
            Event = Event.join(Events_DF, on="TimeUS")
        if in_polars == True: return Event
        else: return Event.to_pandas()
    
    # Function to return Modes details
    def GetModes(self, in_polars=False):
        self._extract('MODE')
        Mode = self.DFdict['MODE'].clone()
        Mode_DF = Mode.apply(lambda column: (column[1], _mode_id[column[2]], _mode_reason[column[-1]])) 
        Mode_DF = Mode_DF.rename({"column_0": "TimeUS", "column_1": "Mode", "column_2": "Reason"})
        Mode.replace('Mode', Mode_DF['Mode'])
        Mode_DF = Mode_DF.drop('Mode')
        Mode = Mode.join(Mode_DF, on="TimeUS")
        if in_polars == True: return Mode
        else: return Mode.to_pandas()
    
    # Function to return PARAMS of mission 
    def GetPARAMS(self, with_datetime = False, in_dict= False, in_polars=False):
        self._extract('PARM')
        if with_datetime: PARM = self.DFdict['PARM'][['DateTime','Name', 'Value']].clone()
        else: PARM = self.DFdict['PARM'][['Name', 'Value']].clone()
        if in_dict == True: return self.DFdecode.params
        elif in_polars == True: return PARM
        else: return PARM.to_pandas()
        
    # Function to return value for PARAM command 
    def GetPARAM(self, command):
        return self.DFdecode.param(command)
    
    # Function to return value for PARAM command 
    def GetPARAM(self, command):
        return self.DFdecode.param(command)
    
    # close the log file
    def close(self):
        self.DFdecode.close()