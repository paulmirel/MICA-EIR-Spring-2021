"""
Provides a simple interface to write csv data.

from timestamp_csv_data import timestamp_and_record

See the help(timestamp_and_record)
"""

import storage, os, board, digitalio, sys
import adafruit_sdcard

path = "/sd/data.csv"
data_fh = None # the state of the (open) file
timestamp_source = None
mounted = False

def setup(spi_bus=None, sdcard_cs_pin=None):
    """Called automatically by timestamp_and_record() the first time.
        Assumes board.SPI(), and board.D10 (should be SD_CS, but that isn't define everywhere).
    """
    global data_fh, mounted

    # None means "haven't tried yet (or was closed)"
    # False means "tried and failed"
    data_fh = False # we (will have) tried

    if not mounted:
        mount_point, delim, rest = path[1:].partition("/") # skip leading /, nb: /sd/bob -> ('', '/', 'sd/bob')
        mount_point = "/" + mount_point
        print("#   setup sd_card and mount as {:}".format(mount_point))

        try:
            spi_bus = spi_bus or board.SPI()
            sdcard = adafruit_sdcard.SDCard( spi_bus, digitalio.DigitalInOut( sdcard_cs_pin or board.D10 ) )
            vfs = storage.VfsFat( sdcard )
            storage.mount( vfs, mount_point )
            mounted = True
        except ValueError as e:
            print('Failed to setup and mount the sdcard as "/sd": {:}'.format(e))
            raise

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

def _open():
    global data_fh

    try:
        if not data_fh:
            data_h = False # we will have tried, None means we haven't tried
            data_fh = open( path, 'a')
    except OSError as e:
        print("Failed to open {:}: {:}".format(path, e))

def timestamp_and_record(*args):
    """
    First, setup with a .datetime() source:
        # like a adafruit_pcf8523 object
        timestamp_and_record( some_real_time_clock ) 
    Then write csv data:
        # Does a "to string" on them as formatting
        # Writes to /sd/data.csv AND the console
        #   We prefix with "DATA: " on the console
        # Always appending to /sd/data.csv
        # Call rotate() to rename current file and start a new one
        timestamp_and_record( v1, v2, v3, v4 )
        and/or
        data = []
        data.append( v1 )
        data.append( v2 )
        ...
        timestamp_and_record( data )
    Each row has the timestamp (presumed utc) as the first value:
        # IFF you did the setup
        YYYYMMDDTHHMMSSZ,values...
        i.e.:
        20210107T155500Z,values...
    """
    global timestamp_source

    # On the first call, try to setup
    if not mounted:
        setup()
    if mounted and data_fh == None:
        _open()

    if len(args) == 1 and getattr(args[0], "datetime", None):
        # the "setup" like call
        print("#   set timestamp_source = {:}".format(args[0]))
        timestamp_source = args[0]
        timestamp_source.datetime # force first use to get early error
        return True

    # on the console prefix:
    sys.stdout.write("DATA: ")
    _timestamp_and_record(sys.stdout, *args)
    if data_fh:
        _timestamp_and_record(data_fh, *args)
        return True
    return False

def _timestamp_and_record(fh, *args):
    """Do the write to the file handle"""

    global timestamp_source

    # figure out if multiple args, a list, or setup
    if len(args) == 1:
        the_arg = args[0]
        if isinstance(the_arg, list) or isinstance(the_arg, tuple):
            # a list == a row
            # we purposefully do NOT do a join, to minimize memory impact

            if timestamp_source:
                dt = timestamp_source.datetime
                iso8601_utc = "{:04}{:02}{:02}T{:02}{:02}{:02}Z".format( dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec)
                fh.write(iso8601_utc)
                fh.write(",") # we know there is more data

            for i,value in enumerate(the_arg):
                if i>0:
                    fh.write(",")
                fh.write( str(value) )
            fh.write("\n")

        elif isinstance(the_arg, str) or isinstance(the_arg, int) or isinstance(the_arg, float) or isinstance(the_arg, bool):
            # degenerate case of a list of values that is 1 long
            _timestamp_and_record(fh, [the_arg])

        else:
            raise Exception("Expected a list, or several arguments, saw {:} {:}".format(the_arg.__class__.__name__,the_arg))

    elif len(args) >= 1:
        # the args are a list, so do that
        _timestamp_and_record(fh, args)

    else:
        raise Exception("You called timestamp_and_record() without any arguments")
        return

def close():
    """
    Usually not necessary. You can continue blithely again after this (it reopens).
    import timestamp_csv_data
    ...
    timestamp_csv_data.close()
    """

    global data_fh
    if data_fh:
        data_fh.close()
    data_fh = None

def rotate():
    """
    Rename current file to /sd/data_YYYYMMDD_HHMMSS.csv, and start a new one.
    import timestamp_csv_data
    ...
    timestamp_csv_data.rotate()
    """
    #print("# rot closing...")
    close()
    # if we get called before anything
    setup()

    name,delim,ext = path.rpartition('.')
    #print("# rot path parsed as {:} ext {:}".format(name,ext))

    vers = None
    exists = False

    try:
        exists = os.stat(path) # will throw if non-existent
        #print("# rot path exists")

    except OSError as e:
        if e.strerror == "No such file/directory":
            # no extant data.csv, so move along
            #print("# rot no {:} yet".format(path))
            pass
        else:
            raise # something else went wrong

    if exists:
        if timestamp_source:
            dt = timestamp_source.datetime
            vers = "{:04}{:02}{:02}_{:02}{:02}{:02}".format( dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec)
            #print("# rot have a ts source so {:}".format(vers))
        else:
            # sigh, find how many and count them
            rest, delim, basename = path.rpartition('/') # basename
            basename, delim, rest = basename.rpartition('.') # strip .ext

            datadir,delim,rest = path.rpartition( '/') # drops leading /
            datadir = datadir
            print("# rot no ts source, so path parses to dir {:}".format(datadir))

            ct = 0
            #print("# rot list 'em vs {:}.|_ ...".format(basename))
            for fname in os.listdir(datadir):
                # could be data.csv or data_YYYYMMM..csv
                print("# rot   consider {:}".format(fname))
                if fname.startswith(basename + ".") or fname.startswith(basename + "_"):
                    ct += 1
                    print("# rot   counts! {:}".format(ct))
            vers = None if ct==0 else str(ct)
            #print("# rot no ts source so ct {:} -> {:}".format(ct, vers))

    if vers:
        new_name = "{:}_{:}.{:}".format( name, vers, ext )
        print("# Renamed {:} -> {:}".format(path,new_name))
        os.rename(path, new_name)

    print("# rot reopen...")
    _open()

