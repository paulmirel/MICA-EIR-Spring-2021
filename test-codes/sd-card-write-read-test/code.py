#record simple file to sd card
#2020-02-09
#Paul Mirel

import time
import adafruit_sdcard
import board
import busio
import digitalio
import storage
import terminalio

#Adalogger Featherwing uses pin D10 for the SDCard chip select line on the SPI bus
#THAT WAS A COLLISION, so I modified the SD card to use pin D11 for chip select
SD_CS = board.D11
spi_bus = board.SPI()
# Connect to the card and mount the filesystem.
sd_cs = digitalio.DigitalInOut( SD_CS )
sdcard = adafruit_sdcard.SDCard( spi_bus, sd_cs )
vfs = storage.VfsFat( sdcard )
storage.mount( vfs, "/sd" )
# Files are under /sd

with open( "/sd/test.txt", "w" ) as f:
    f.write( "year month day batch checksum" )
    
    
with open("/sd/test.txt", "r") as f:
    print("Printing lines in file:")
    line = f.readline()
    while line != '':
        print(line)
        line = f.readline()
print( "Program Completed" )