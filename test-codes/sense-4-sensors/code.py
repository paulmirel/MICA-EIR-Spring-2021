"""
Read the 4 gesture sensors independently
"""

from board import SCL, SDA
import busio
import time
from apds9660_extended import APDS9960_Extended

print("Connect to apds9660 on i2c...")

i2c = busio.I2C(SCL, SDA)

first_fail = True
apds = None
while not apds:
    try:
        apds = APDS9960_Extended(i2c)
    except ValueError as e:
        if "No I2C device at address" in str(e):
            if first_fail:
                print("apds9660: {:}".format(e))
                print("Plug it in, I'll keep looking...")
                first_fail = False
            apds = None
            time.sleep(0.25) # wait for plugin
        else:
            raise(e)

print("Found apds9660")

apds.enable_gesture = True

# Uncomment and set the rotation if depending on how your sensor is mounted.
# apds.rotation = 270 # 270 for CLUE

while True:
    data = apds.gesture_data()

    if data:
        print("{:3} {:3} {:3} {:3}".format( data.up, data,down, data.left, data.rigth ))
