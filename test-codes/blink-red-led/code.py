import time
import board
import digitalio

print("Initializes the built-in LED pin");
print("Then watch me for 1 second blink");

try:
    indicator_LED = digitalio.DigitalInOut( board.D13 )
    indicator_LED.direction = digitalio.Direction.OUTPUT
    indicator_LED.value = True #active low, True is off
    print( "initialized indicator" )
except Exception as err: # FIXME: identify some typcial errors
    print( "Error: led pin init failed {:}".format(err) )

while True:
    indicator_LED.value = 1
    time.sleep( 1 )
    indicator_LED.value = 0
    time.sleep( 1 )
