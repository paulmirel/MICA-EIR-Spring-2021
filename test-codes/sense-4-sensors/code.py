"""
Read the 4 gesture sensors independently,
and print them: [up,down,left,right]
Try running processing/sensors_4 to visualize the data.
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
print("Trigger activity by getting very close to sensor")

apds.enable_proximity = True
apds.enable_gesture = True

# Uncomment and set the rotation if depending on how your sensor is mounted.
# apds.rotation = 270 # 270 for CLUE

def exp_smooth_one(old, raw_value, factor):
    return raw_value / factor + old - old / factor;

def exp_smooth_array( sofar, raw ):
    """mutates"""
    for i, val in enumerate(raw):
        sofar[i] = exp_smooth_one( sofar[i], val, 10 )

smoothed = [0,0,0,0]
prev = smoothed.copy()

while True:
    # nb: the sensor datasheet calls the values:
    # left,right,up,down
    # (which makes sense if you are looking for direction of motion)
    # BUT, the actual sensor is the reflected one,
    # so really:
    # right,left,down,up
    data = apds.gesture_data()

    if data:
        exp_smooth_array(smoothed, data)

        diff = False
        for i,val in enumerate(prev):
            if int(smoothed[i]) != int(val):
                diff = True
                break;
        prev = smoothed.copy()
        # only  print if different
        if diff:
            # our processing sketch is relying on this exact format:
            # leading [
            # no spaces, comma seperated, 4 int values (0..255)
            # AND
            # remembering that the sensor values are reflected
            # and we want to print up,down,left,right
            # we reflect here:
            print("[{:03.0f},{:03.0f},{:03.0f},{:03.0f}]".format( smoothed[1], smoothed[0], smoothed[2], smoothed[3] ))
