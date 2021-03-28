"""
Set the RTC from the console.
"""

import busio
import adafruit_pcf8523
import time
import board
from sys import stdin,stdout

myI2C = busio.I2C(board.SCL, board.SDA)
print("I2C setup")
rtc = adafruit_pcf8523.PCF8523(myI2C)
print("RTC setup")
battery_low = rtc.battery_low
if battery_low:
    print( "Clock battery is low. Replace the clock battery." )
else:
    print( "Clock battery voltage is OK." )

days = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")

def show_timedate():
    timenow = rtc.datetime
    print("%s %d-%d-%d %d:%02d:%02d" % (
        days[timenow.tm_wday], timenow.tm_year, timenow.tm_mon, timenow.tm_mday,
        timenow.tm_hour, timenow.tm_min,timenow.tm_sec
        ))

show_timedate()

print()
print("Set time. Does not take effect untill final 'set now?' question. Load some other code, or use ^c to quit")

def readline_echo():
    # we want to echo each character as it is typed, then return the result at EOL
    sofar = ''
    while True:
        c = stdin.read(1)
        # only accept numbers
        if c >= '0' and c<= '9':
            sofar += c
            stdout.write(c)
        elif c == "\n":
            print()
            if len(sofar) == 0:
                return sofar # take default
            else:
                return int(sofar)

def ranged_input(prompt, acceptable_range, default):
    # accept an integer in the range
    # remember range(a,b) is from a to <b
    while(True):
        stdout.write( "{:10} ({:}..{:}) [{:}]? ".format(prompt, acceptable_range.start, acceptable_range.stop-1, default) )
        value = readline_echo()
        if value == "":
            return default
        elif value in acceptable_range:
            return value
        print("  Expected a number {:}..{:}".format( acceptable_range.start, acceptable_range.stop-1 ))

t = rtc.datetime

print()
print("Set time and date. Just hit enter to keep same value)")
try:
    # catch the ^c...

    # remember the .stop value of range is 1 greater than you want
    year = ranged_input("Year", range(2000,2101), t.tm_year) # 2000 is actual minimum!
    month = ranged_input("Month", range(1,13), t.tm_mon+1) 
    day = ranged_input("Day", range(1,32), t.tm_mday) 
    weekday = ranged_input("Week Day (Sunday=1)", range(1,8), t.tm_wday+1)
    print()
    print("Enter a time a little in the future, the last prompt (set now?) will set it.")
    hour = ranged_input("Hour", range(0,24), t.tm_hour) 
    min = ranged_input("Minute", range(0,60), t.tm_min) 
    sec = ranged_input("Second", range(0,60), t.tm_sec) 

    t = time.struct_time((year,  month-1,   day,   hour,  min,  sec,    weekday-1,   -1,    -1))
    #print(t)

    stdout.write("Set now (^C for No)? ")
    stdin.readline()

    rtc.datetime = t
    print("Set!")
    #print(rtc.datetime)
    print()

except KeyboardInterrupt:
    print("Ok, nothing changed. Watch the time for 5 seconds, then done")

for i in range(0,5): # 0..4
    time.sleep(1) # wait a second
    print("\n",i+1)
    show_timedate();

print("program completed")
print("^D to re-run to set time/date")
