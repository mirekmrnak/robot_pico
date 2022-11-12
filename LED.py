#pin26 IN
#pin27 OUT
from machine import Pin
from time import sleep
import neopixel

#definování konstant a barev
np = neopixel.NeoPixel(Pin(26, Pin.OUT), 8)
headlights = (0, 3)
backlights = (5, 6)
led_white = (60, 60, 60)
led_red = (60, 0, 0)
led_off = (0, 0, 0)
led_red_br = (255, 0, 0)
led_orange = (100, 35, 0)
indicator_left = (1, 4)
indicator_right = (2, 7)
indicator_warning = (1, 2, 4, 7)

def carON():
    for x in range(20):
        for a in range(0, 8):
            np[a] = led_orange
        np.write()
        sleep((120-(x*5))/1000)
        lightsOFF()
        sleep((120-(x*5))/1000)

def lightsON():
    for x in headlights:
        np[x] = led_white
    for x in backlights:
        np[x] = led_red
    np.write()

def lightsOFF():
    for x in headlights:
        np[x] = led_off
    for x in backlights:
        np[x] = led_off
    np.write()

def lightsWarning():
    for x in headlights:
        np[x] = led_red_br
    for x in backlights:
        np[x] = led_red_br
    np.write()

def lightsBreakON():
    for x in backlights:
        np[x] = led_red_br
    np.write()

def lightsBreakOFF():
    pass

def lightsIndicator(direction):
    for x in direction:
        np[x] = led_orange
    np.write()
    sleep(0.2)
    for x in direction:
        np[x] = led_off
    np.write()
    sleep(0.2)
        

#testování všech funkcí světel
if __name__ == '__main__':
    while True:
        lightsON()
        sleep(2)
        lightsBreakON()
        sleep(2)    
        lightsOFF()
        sleep(2)
        lightsIndicator(indicator_left)
        lightsIndicator(indicator_right)
        lightsIndicator(indicator_warning)
