import time
import board
import neopixel

#initialize the neopixel
NEOPIXEL_PIN = 8
pixel = neopixel.NeoPixel(board.NEOPIXEL, NEOPIXEL_PIN, brightness=1, auto_write=False)
pixel.fill((0, 0, 255))
pixel.show()
time.sleep(3)
