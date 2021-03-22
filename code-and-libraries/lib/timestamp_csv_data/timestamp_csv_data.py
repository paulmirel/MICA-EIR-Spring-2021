"""
Provides a simple interface to write csv data, with access to more detailed control via an object(s).
Each line of data has a timestamp prefix, and is comma-seperated.
Each line is echoed to sys.stdout
Options allow writing the data as name,units,precision,value for each value.

#### Simplest interface, "inline", just values
# (a bunch of defaults)
import timestamp_and_record from timestamp_csv_data

set up your sensors etc...

while(True):
    ...
    # "inline" writing data without fieldnames:
    # Any number of values, should be numeric.
    # Will try to use: board.SPI(), and board.D11 for sd-card-CS, mounting it as /sd.
    # Will write one line of data to the default datafile /sd/data.csv
    # (This will write data at the maximum speed of this `while` loop!)
    timestamp_csv_data( sensor1.readcolor(), analog1.read(), sensor3.getTemperature() )

#### Simple interface, "accumulate a list" 
# Almost as simple as above
# (you can also use an `array` here instead of a list)
import timestamp_and_record from timestamp_csv_data

set up your sensors etc...

while(True):
    ...
    # "accumulating" might make more sense for you
    data = []
    # add data to the list, again, should be numeric.
    data.append( sensor1.readcolor() )
    ...
    data.append( analog1.read() )
    ...
    data.append( sensor3.getTemperature() )
    ...
    # etc.

    # writing a list without fieldnames
    # Like the above, but using a list
    timestamp_csv_data( data )
"""

import storage, os

class TimeStampCSV:
    def __init__(self, path="/sd/data.csv", automount=None, timestamp=None):
        """
            path = location of datafile, will mkdir
            automount =  { "path" : "/sd1", "spi" : board.SPI(), "CS" : board.SD_CS }
                All parts are optional
            timestamp =
                None : no timestamp prefix
                some-rtc-device : with a .datetime property, like the adafruit_pcf8523
        """
        # FIXME: the assumptions that go into timestamp=True are overly specific to our hardware

        self.fh = None # serves as a flag too

        if automount:
            import adafruit_sdcard, digitalio
            spi_bus = automount['spi'] or board.SPI()
            sdcard = adafruit_sdcard.SDCard( spi_bus, digitalio.DigitalInOut( automount["CS"] or board.SD_CS ) )
            vfs = storage.VfsFat( sdcard )
            storage.mount( vfs, automount['path'] )

        path_dir, delim, leaf = path.rpartition("/")
        try:
            os.mkdir( path_dir )
        except OSError as e:
            if e.strerror == "Read-only filesystem":
                # when readonly
                print("Warning: reado-only filesystem on {:}, not logging".format(path_dir))
                return
            elif e.strerror == "File exists":
                # good, it got mounted
                pass
            else:
                raise # who knows

        self.timestamp = timestamp

        self.fh = open( path, 'w')
        self.beginning_of_line = True

    def write(self, *args, units=None, format=None, precision=None):
        """
        Writes values with optional parts (see "args" below):
            # up to 4 parts for each value:
            name,units,precision,value,...
        Each row has the timestamp (presumed utc) as the first value:
            YYYYMMDDTHHMMSSZ,values...
            i.e.:
            20210107T155500Z,values...

        optional:
            units is a string 
                default is to omit
            format is a string.format argument, like "{:03.1f}"
                default is "{:}", i.e. str()
            precision is string
                default is to omit
        args can be:
            One value at a time:
                # format is optional
                write(somevalue, format="{:03.1f}" ) # no other arguments
                write(...) # next value
                # You must end the row:
                write() # end row
            Name and value, and extra info, one at a time:
                # extra info is optional
                write("itsname", itsvalue, units=...,format=..., precision=...)
                write(...)
                # You must end the row:
                write()
            A whole row of just values:
                write( [1,3,4] )
            A whole row of names and values:
                write( {"name1" : 1, "name2" : 2 } )
        """

        if not self.fh:
            return

        if self.beginning_of_line and self.timestamp:
            dt = self.timestamp.datetime
            iso8601_utc = "{:04}{:02}{:02}T{:02}{:02}{:02}Z".format( dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec)
            self.fh.write(iso8601_utc)
            self.beginning_of_line = False

        # python don't do multi-methods...
        if len(args) == 0:
            #print("WRITE END",args)
            self.fh.write("\n")
            self.beginning_of_line = True
        elif len(args) == 1:
            if isinstance( args[0], dict ):
                #print("WRITE dictish",args)
                for name,value in args[0].items():
                    self.write( name, value )
                self.write()
            elif isinstance( args[0], tuple) or isinstance( args[0], list ):
                #print("WRITE listish",args)
                self.fh.write(",")
                self.fh.write( ",".join(str(x) for x in args[0]) )
                self.write()
            elif len( args ) == 1:
                #print("WRITE v-only",args)
                if not self.beginning_of_line:
                    self.fh.write(",")
                if format:
                    self.fh.write(format.format(args[0]))
                else:
                    self.fh.write("{:}".format(args[0]))
                self.beginning_of_line = False
            else:
                raise Exception( "Expected list, dict, value or k,v. Saw",args );
        elif len( args ) == 2:
            #print("WRITE kv",*args)
            if not self.beginning_of_line:
                self.fh.write(",")

            self.fh.write(args[0])
            if units:
                self.fh.write( ",")
                self.fh.write( units )
            if precision:
                self.fh.write( ",")
                self.fh.write( precision )
            self.fh.write(",")
            if format:
                self.fh.write(format.format(args[1]))
            else:
                self.fh.write( "{:}".format(args[1]) )
            self.beginning_of_line = False

        else:
            raise Exception( "Expected list, dict, value or k,v,.... Saw",args );
            
        #print("      format={:} units={:} prec={:}".format(format,units,precision))

    def close(self):
        self.fh.close()
