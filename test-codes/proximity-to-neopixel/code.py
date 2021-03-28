"""
Demonstrate sensor to indicator.

In this case, read proximity sensor and show as hue on neopixel.
"""
import time

# Setup I2C 
from board import SCL, SDA
import busio
i2c = busio.I2C(SCL, SDA) # a ValueError typically means something got leftover. do a reset.
print("I2C setup")

# Setup for proximity sensor
from adafruit_apds9960.apds9960 import APDS9960

apds_first_fail = True

def wait_for_apds():
    # can be adapted to wait for any I2C device
    global apds_first_fail # suggests this should be a little class
    device = None
    while not device:
        try:
            device = APDS9960(i2c) # the only thing to change for different device
        except ValueError as e:
            if "No I2C device at address" in str(e):
                if first_fail:
                    # Say that we didn't find it, and say we are waiting
                    print("{:}: {:}".format(device.__class__.__name__, e))
                    print("Plug it in, I'll keep looking...")
                    first_fail = False
                device = None
                time.sleep(0.25) # wait for plugin
            else:
                raise(e)
    print("Found and setup {:}".format(device.__class__.__name__))
    return device

apds = wait_for_apds()
apds.enable_proximity = True

print("hello")

