import board
import time
import busio
import adafruit_pcf8523
from analogio import AnalogIn

vbat_voltage_pin = AnalogIn(board.VOLTAGE_MONITOR)

I2C_bus = busio.I2C(board.SCL, board.SDA)
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
