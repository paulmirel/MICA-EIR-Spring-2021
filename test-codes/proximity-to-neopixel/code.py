"""
Demonstrate sensor to indicator.

In this case, read proximity sensor and show as hue on neopixel.
"""

import board
import busio
from adafruit_apds9960.apds9960 import APDS9960
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

# Setup I2C (apds9960 is an i2c device)
i2c = busio.I2C(board.SCL, board.SDA) # a ValueError typically means something got leftover. do a reset.
print("I2C setup")

# Setup for proximity sensor

def wait_for_apds():
    # can be adapted to wait for any I2C device
    apds_first_fail = True
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

# turn on proximity detector
apds.enable_proximity = True

# setup neopixel
NEOPIXEL_PIN = 8
# (yikes, this is very bright, make brightness less if it annoys you)
pixel = neopixel.NeoPixel(board.NEOPIXEL, NEOPIXEL_PIN, brightness=1, auto_write=False)
pixel.fill((255, 255, 255)) # start as white (quickly changes to show maximum distance which is red)
pixel.show()
print("Neopixel setup (white)")

# Read and update neopixel
print("Show proximity as hue...")
while True:
    # detects out to about 8cm for me.
    # weird, my finger gives 0..250, but my whole hand only does 0..50
    value = apds.proximity

    if value > 8:
        # values < 2 are boring to print
        print( value )

    # we can use 0..255 from the proximity as the hue
    # so much easier in HSV
    # (but notice that "close", i.e. 250, is purple (blue+red), try to fix this to only go to full-blue)
    # More fun stuff with fancy:
    #   https://learn.adafruit.com/fancyled-library-for-circuitpython/led-colors#secret-ingredient-gamma-correction-2981395-9
    #   full docs at
    #   https://circuitpython.readthedocs.io/projects/fancyled/en/latest/api.html
    hsv_color = fancy.CHSV( value )

    # neopixel only speaks rgb
    rgb_color = fancy.CRGB( hsv_color )
    pixel[0] = rgb_color.pack() # convert e.g. 0xFF1200, "int" style
    pixel.show()
