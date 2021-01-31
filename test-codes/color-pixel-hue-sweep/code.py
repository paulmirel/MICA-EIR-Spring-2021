import time
import board
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

#initialize the neopixel
NEOPIXEL_PIN = 8
pixel = neopixel.NeoPixel(board.NEOPIXEL, NEOPIXEL_PIN, brightness=1, auto_write=False)
pixel.fill((0, 0, 0))
pixel.show()

hue = 0.0
sat = 1.0
val = 1.0

while True:
    hue = 0
    while hue < 1:
        #print( hue )
        color_hsv = fancy.CHSV( hue ) #input 0 to 1 for H, S, V :: OK to send only Hue
        color_RGB_normalized = fancy.CRGB( color_hsv )
        color_RGB = fancy.denormalize( color_RGB_normalized )
        #print( color_RGB )
        pixel.fill(( color_RGB ))
        hue = hue + 0.01
        time.sleep( 0.02 )
        pixel.show()
    time.sleep(1.1)