import time
import board
import neopixel

#initialize the neopixel
NEOPIXEL_PIN = 8
pixel = neopixel.NeoPixel(board.NEOPIXEL, NEOPIXEL_PIN, brightness=1, auto_write=False)
OFF = ( 0, 0, 0 )

#set the brightness to something a little less blinding
pixel.brightness = 0.2

while True:
    pixel.fill(( 0, 0, 255 )) #(( red_amount, green_amount, blue_amount )) amount range is 0 - 255
    pixel.show()
    time.sleep( 1 )
    pixel.fill( OFF )
    pixel.show()
    time.sleep(1)
