import time
import board
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

#initialize the neopixel
NEOPIXEL_PIN = 8
pixel = neopixel.NeoPixel(board.NEOPIXEL, NEOPIXEL_PIN, brightness=1, auto_write=False)
OFF = ( 0, 0, 0 )

#set color by HSV, range 0.0 to 1.0
hue = 0.0
sat = 1.0 #color saturation
val = 1.0 #color value = brightness

while True:
    #convert HSV to RGB
    color_hsv = fancy.CHSV( hue ) #input 0 to 1 for H, S, V :: OK to send only Hue
    color_RGB_normalized = fancy.CRGB( color_hsv )
    color_RGB = fancy.denormalize( color_RGB_normalized )


    pixel.fill( color_RGB ) #(( red_amount, green_amount, blue_amount )) amount range is 0 - 255
    pixel.show()
    time.sleep( 1 )
    pixel.fill( OFF )
    pixel.show()
    time.sleep(1)
