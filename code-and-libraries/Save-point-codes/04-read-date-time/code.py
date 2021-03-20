import time
import board
import digitalio
import busio
import adafruit_pcf8523

#Initialize LED
try:
    indicator_LED = digitalio.DigitalInOut( board.D13 )
    indicator_LED.direction = digitalio.Direction.OUTPUT
    indicator_LED.value = 1 #active low, 1 is off
    print( "initialized indicator" )
except Exception as err:
    print( "Error: led pin init failed {:}".format(err) )

#Initialize I2C communications bus
try:
    I2C_BUS= busio.I2C(board.SCL, board.SDA)
except Exception as err:
    print( "Error: I2C bus init failed {:}".format(err) )


#Initialize Real Time Clock
try:
    rtc = adafruit_pcf8523.PCF8523(I2C_BUS)
except Exception as err:
    print( "Error: Real Time Clock init failed {:}".format(err) )

days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

#Set the clock here:
if False: #True: #False  # change to True if you want to write the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2021,  03,   14,   18,  00,  00,    0,   -1,    -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time

    print("Setting time to:", t)     # uncomment for debugging
    rtc.datetime = t
    print()

#main program loop begins here

while True:
    timenow = rtc.datetime
    print("The date is %s %d-%d-%d" % (days[timenow.tm_wday], timenow.tm_year, timenow.tm_mon, timenow.tm_mday))
    print("The time is %d:%02d:%02d" % (timenow.tm_hour, timenow.tm_min,timenow.tm_sec))
    indicator_LED.value = 0
    time.sleep(0.5)
    indicator_LED.value = 1
    time.sleep(0.5)
