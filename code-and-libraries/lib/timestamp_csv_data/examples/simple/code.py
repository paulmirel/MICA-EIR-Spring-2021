"""
Write data testing.

Assumes: adafruit_sdcard using featherwing adalogger spi with CS=D10
"""

# The key:
from timestamp_csv_data import timestamp_and_record

# we'll need to setup the rtc
import board,busio
import adafruit_pcf8523

# only for this testing code
import timestamp_csv_data # normal people don't need this, we do tricky stuff to test
import sys

def diff(row_number, file_data, expected):
    """For the testing: After we write, tell if the file_data is what we expected"""
    print("line",row_number)
    bad = False

    # drop timestamp
    if expected.startswith('YYYYMMDDTHHMMSSZ'):
        ts1,delim,expected = expected.partition(",")
        ts2,delim,file_data = file_data.partition(",") 
    else:
        ts1 = ""
        ts2 = ""

    for i,c in enumerate(expected):
        if i > len(file_data) - 1:
            bad = True
            break
        if expected[i] != file_data[i]:
            bad = True
            break
    if bad:
        i += len(ts1) + 1
        print("   ", ts1 + "," + expected)
        sys.stdout.write("F:  " + ts2 + "," + file_data)
        if len(file_data) == 0:
            print("")
        print( "@:  " + (" " * i) +  "^" )
    else:
        sys.stdout.write("OK: ")
        sys.stdout.write(ts2 + ",")
        sys.stdout.write(file_data)


# SETUP

# We want the RTC for timestamps (it is optional)
print("# Setup PCF8523")
myI2C = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_pcf8523.PCF8523(myI2C)

print("# Setup timestamp_and_record")
if not timestamp_and_record( rtc ):
    print("#  failed!")

# We want to rotate the data.csv file, because we are testing
# You don't need to
print("# Rotate /sd/data.csv to get an empty one")
timestamp_csv_data.rotate() # old one is named by the datetime of now


# DO WORK (in this case, testing)

print("# Write a single value")
if not timestamp_and_record(1):
    print("#  failed!")

print("# Write multiple values")
if not timestamp_and_record( 2.0, 2.1 ):
    print("#  failed!")

print("# Write a list")
data = [ 3.0, 3.1, 3.2, 3.3 ]
if not timestamp_and_record( data ):
    print("#  failed!")

print("# close and reopen w/o timestamp-source")
timestamp_csv_data.close()
timestamp_csv_data.timestamp_csv_data.timestamp_source = None # don't do this in your code

print("# Append w/o timestamp")
timestamp_and_record( 4.0, 4.1 )

# Check
timestamp_csv_data.close()
print("# Writing done")

print("# Check data vs expected")
try:
    with open("/sd/data.csv","r") as fh:
        diff(1, fh.readline(), "YYYYMMDDTHHMMSSZ,1")
        diff(2, fh.readline(), "YYYYMMDDTHHMMSSZ,2.0,2.1")
        diff(3, fh.readline(), "YYYYMMDDTHHMMSSZ,3.0,3.1,3.2,3.3")
        diff(4, fh.readline(), "4.0,4.1")
except OSError as e:
    print("Failed to read data from /sd/data.csv",e)
print("# Done")
