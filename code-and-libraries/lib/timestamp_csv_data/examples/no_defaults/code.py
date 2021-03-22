"""
Write data with full control, no defaults.

Assumes: adafruit_sdcard using featherwing adalogger spi with CS=D11
"""
from timestamp_csv_data import TimeStampCSV 

import board,sys,busio
import adafruit_pcf8523

def diff(row_number, file_data, expected):
    """Tell if the file_data is what we expected"""
    print("line",row_number)
    bad = False

    # drop timestamp
    ts1,delim,expected = expected.partition(",")
    ts2,delim,file_data = file_data.partition(",") 

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


myI2C = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_pcf8523.PCF8523(myI2C)

print("# Setup a TimeStampCSV")
csv = TimeStampCSV(
    path = "/sd1/data1.csv",
    automount = { "path" : "/sd1", "spi" : board.SPI(), "CS" : board.D10 },
    timestamp = rtc
    )

print("# Write some rows")
# by field
# NB: avoid comma and double-quotes or you will break csv readers
csv.write( "d1", 1, units = "furlongs/fortnight", precision = "2 paces", format = "{:07.4f}" ) 
# nb, formatting will round!
csv.write( "d2", 2, units = "mW/book", precision = "e-6", format = "{:#3.1f}" ) 
csv.write()

# by tuple or list
csv.write( (3,4,5 ) )
csv.write( [3.1,4.1,5.1 ] )

# by dict
# DANGER: currently, this is reverse-order preserved!
csv.write( { "d4" : 4, "d5" : "{:02d}".format(5) } )

# by value
csv.write(6)
csv.write(7)
csv.write()

# Check
csv.close()
print("# Writing done")

print("# Check data vs expected")
try:
    with open("/sd1/data1.csv","r") as fh:
        diff(1, fh.readline(), "YYYYMMDDTHHMMSSZ,d1,furlongs/fortnight,2 paces,01.0000,d2,mW/book,e-6,2.0")
        diff(2, fh.readline(), "YYYYMMDDTHHMMSSZ,3,4,5")
        diff(3, fh.readline(), "YYYYMMDDTHHMMSSZ,3.1,4.1,5.1")
        # if the order is backwards, then we are finally insertion-order-preserved. fix it here
        diff(4, fh.readline(), "YYYYMMDDTHHMMSSZ,d5,05,d4,4")
        diff(4, fh.readline(), "YYYYMMDDTHHMMSSZ,6,7")
except OSError as e:
    print("Failed to read data from /sd1/data1.csv",e)
print("# Done")
