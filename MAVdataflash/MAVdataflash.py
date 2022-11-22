import datetime
from pymavlink import DFReader as DF
import polars as pl
import matplotlib.pyplot as plt
from MAVdataflash.DataFlashDict import __dtypes__, __dunits__, __event_id__

class DataFlash:
    
    DFdict = {}   # Dictionary of all dtypes
    DFunit = {}  # Dictionary for dtypes units
    
    def __init__(self, filename):
        self.filename = filename
        
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
                DFdict['Columns'].insert(0, "DateTime")
                DFdict['Format'] = list(DFdict['Format'])
                DFdict['Format'].insert(0, "DT")
                # Initializing DataFrame with FMT message 
                DFcolumns_init = [pl.Series(column, dtype= __dtypes__[dtype]) for column, dtype in zip(DFdict['Columns'], DFdict['Format'])]
                self.DFdict[DFdict['Name']] = pl.DataFrame(DFcolumns_init)
            elif DFdict['mavpackettype'] == 'FMTU':
                DFdict['UnitIds'] = list(DFdict['UnitIds'])
                DFdict['UnitIds'].insert(0, "-")
                # Exctracting Units and mutliplier for columns
                self.DFunit[self.DFdecode.id_to_name[DFdict['FmtType']]] = {column: __dunits__[unit] 
                        for column, unit in zip(self.DFdict[self.DFdecode.id_to_name[DFdict['FmtType']]].columns, DFdict['UnitIds'])}
                            
    def __extract__(self, dtype):
        DFlist = []
        if self.DFdict[dtype].shape[0] == 0:
            while 1:
                # extract the data type
                DFmsg = self.DFdecode.recv_match(type=dtype)
                if DFmsg is None:
                    self.DFdecode.rewind()
                    break
                DFdict = DFmsg.to_dict()
                if 'mavpackettype' in DFdict: del DFdict['mavpackettype']
                DFdict = {'DateTime': datetime.datetime.fromtimestamp(DFmsg._timestamp), **DFdict}
                # list append of DFmsg
                DFlist.append(DFdict)
            if len(DFlist) != 0:
                # updating dataframe from DF list
                Data = pl.DataFrame(DFlist)
                Data = Data.with_columns(pl.col("DateTime").dt.cast_time_unit(tu="ms"))
                self.DFdict[dtype] = pl.concat([self.DFdict[dtype], Data], how='diagonal')
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
    def GetData(self, dtype, in_polars=False):
        self.__extract__(dtype)
        if in_polars == True: return self.DFdict[dtype]
        else: return self.DFdict[dtype].to_pandas()

    # Function to plot the data
    def Plot(self, dtype, column, instance=None):
        if self.isPlotable(dtype, column=column) == True:
            self.__extract__(dtype)
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
        self.__extract__('EV')
        Event = self.DFdict['EV'].clone()
        Events_DF = Event.apply(lambda column: (column[1], __event_id__[column[2]]))
        Events_DF = Events_DF.rename({"column_0": "TimeUS", "column_1": "Event"})
        Event = Event.join(Events_DF, on="TimeUS")
        if in_polars == True: return Event
        else: return Event.to_pandas()
    
    # Function to return PARAMS of mission 
    def GetPARAMS(self, in_polars=False):
        self.__extract__('PARM')
        PARM = self.DFdict['PARM'][['Name', 'Value']].clone()
        if in_polars == True: return PARM
        else: return PARM.to_pandas()
        
    # Function to return value for PARAM command 
    def GetPARAM(self, command):
        return self.DFdecode.param(command)