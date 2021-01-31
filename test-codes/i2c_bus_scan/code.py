# CircuitPython I2C scan

# bus addresses
# 0x77 -- environmental sensor -- BME680
# 0x39 -- local sensor -- APDS9960
# 0x3c -- OLED display -- SH1107
# 0x68 -- Real time clock - PCF8523 - 0x68

import time

import board
import busio

i2c = busio.I2C(board.SCL, board.SDA)

while not i2c.try_lock():
    pass

while True:
    print("I2C addresses found:", [hex(device_address)
                                   for device_address in i2c.scan()])
    time.sleep(2)
