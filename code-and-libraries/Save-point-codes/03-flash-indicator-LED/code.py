import time
import board
import digitalio

try:
    indicator_LED = digitalio.DigitalInOut( board.D13 )
    indicator_LED.direction = digitalio.Direction.OUTPUT
    indicator_LED.value = 1 #active low, 1 is off
    print( "initialized indicator" )
except Exception as err:
    print( "Error: led pin init failed {:}".format(err) )


while True:
    print("Hello")
    indicator_LED.value = 0
    time.sleep(0.5)
    indicator_LED.value = 1
    time.sleep(0.5)
