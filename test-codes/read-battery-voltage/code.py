import board
import time
import busio
import adafruit_pcf8523
from analogio import AnalogIn

print("Print the main-voltage, and rtc board battery status")
print("Over and Over again")

vbat_voltage_pin = AnalogIn(board.VOLTAGE_MONITOR)

try:
    I2C_bus = busio.I2C(board.SCL, board.SDA)
except ValueError as e:
    if "Invalid pins" in str(e):
        print("Sadly, the SCL and/or SDA didn't get released properly on some previous run")
        print("So, sadly, you have to press reset")
        sys.exit(1)
    else:
        print("Something went wrong during busio.I2C() init")
        raise(e)

rtc = adafruit_pcf8523.PCF8523(I2C_bus)


def get_voltage( pin ):
    return ( pin.value * 3.3 ) / 65536 * 2

while True:
    battery_voltage = round( get_voltage( vbat_voltage_pin ), 2 )

    #check clock battery OK
    if ( rtc.battery_low ):
        clock_battery_status = "LOW"
    else:
        clock_battery_status = "OK"
    print( "Main Battery voltage: {}   Clock Battery status: {}".format( battery_voltage, clock_battery_status ) )

    time.sleep( 1 )
