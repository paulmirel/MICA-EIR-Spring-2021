# CircuitPython I2C scan

# bus addresses
# 0x77 -- environmental sensor -- BME680
# 0x39 -- local sensor -- APDS9960
# 0x3c -- OLED display -- SH1107
# 0x68 -- Real time clock - PCF8523 - 0x68

import time

import board
import busio
import sys

print("Initializes the busio.I2C")
print("Then, every 2 seconds")
print("shows you the result of i2c.scan()")

i2c = None

try:
    i2c = busio.I2C(board.SCL, board.SDA)
except ValueError as e:
    if "Invalid pins" in str(e):
        print("Sadly, the SCL and/or SDA didn't get released properly on some previous run")
        print("So, sadly, you have to press reset")
        sys.exit(1)
    else:
        print("Something went wrong during busio.I2C() init")
        raise(e)

while not i2c.try_lock():
    pass

while True:
    print("I2C addresses found:", [hex(device_address)
                                   for device_address in i2c.scan()])
    time.sleep(2)
