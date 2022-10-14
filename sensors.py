# Ultra Sound Sensor, proximity sensors, Line follow sensors
from machine import Pin
from utime import sleep_us, ticks_us

# Sensors connections
proximity_left = Pin(16, Pin.IN)    # Physical pin 21, orange wire
proximity_right = Pin(17, Pin.IN)   # Physical pin 22, orange wire
trigger = Pin(18, Pin.OUT)          # Physical pin 24, green wire
echo = Pin(19, Pin.IN)              # Physical pin 25, blue wire
''''
line_follow_left = Pin(44, Pin.IN)
line_follow_middle = Pin(55, Pin.IN)
line_follow_right = Pin(55, Pin.IN)
'''


# Constants
# journey time (timepassed) by the speed of sound (343.2 m/s, which is 0.0343 cm per microsecond)
c_moded = 0.03432

def distance():
    # function activates the Ultrasound Sensor and gives back time which signal has treveled

    trigger.low()
    sleep_us(2)
    # Sends the sound pulse
    trigger.high()
    sleep_us(5)
    trigger.low()
    # Gets the starting time and arrival of the pulse
    while echo.value() == 0:
        signal_off = ticks_us()
    while echo.value() == 1:
        signal_on = ticks_us()

    # Calculates the time for which signal has traveled
    time_passed = signal_on - signal_off
    distance_ultra = (time_passed * c_moded) / 2

    return distance_ultra

def obstacles():
    # function checks obstacles
    # returns list, where 1st - left sensor, 2nd - right sensor
    # values: 1 - free, 0 - obstacle
    
    return [proximity_left.value(), proximity_right.value()]

def datafromsensors():
    # function calculates the distance and collects data from other sensors

    return [distance(), obstacles()[0], obstacles()[1]]

# test for the file
if __name__ == '__main__':
    print(datafromsensors())