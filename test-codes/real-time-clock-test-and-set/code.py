import busio
import adafruit_pcf8523
import time
import board

myI2C = busio.I2C(board.SCL, board.SDA)
rtc = adafruit_pcf8523.PCF8523(myI2C)

days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

if False: #True: #False  # change to True if you want to write the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2020,  08,   27,   18,  38,  00,    4,   -1,    -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time

    print("Setting time to:", t)     # uncomment for debugging
    rtc.datetime = t
    print()

while True:
    timenow = rtc.datetime
    #print(t)     # uncomment for debugging
    print()
    battery_low = rtc.battery_low
    if battery_low:
        print( "Clock battery is low. Replace the clock battery." )
    else:
        print( "Clock battery voltage is OK." )
    print("The date is %s %d-%d-%d" % (days[timenow.tm_wday], timenow.tm_year, timenow.tm_mon, timenow.tm_mday))
    print("the day of the month is %d" % (timenow.tm_mday))
    print("the month is %d" % (timenow.tm_mon))
    print("The time is %d:%02d:%02d" % (timenow.tm_hour, timenow.tm_min,timenow.tm_sec))

    time.sleep(1) # wait a second
print("program completed")