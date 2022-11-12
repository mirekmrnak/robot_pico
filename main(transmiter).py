# Import the required modules
import microbit
import radio
from timer import Timer

# Switch on the radio hardware
radio.on()

# Definition of variables for data transfer
data0 = "0000"
data1 = "0"
mode = 0
data = "000000"

mode_time = Timer(3)

def zfl(s, width):
    return '{:0>{w}}'.format(s, w=width)

# query loop
while True:
    a = microbit.accelerometer.get_values() # read the accelerometer values
    
    microbit.display.show(mode)

    # Tilt in x and y direction & recalculation to two two digit number -> two position in string & set up max and min vallues
    x = max(min(98, round(int(a[1] / 20) + 49)), 0)
    y = max(min(98, round(int(a[0] / 20) + 49)), 0)

    #Set up data string with ficed number of positions (function zfl)
    data0 = zfl(str(x), 2) + zfl(str(y), 2)

# Assign the letters to a button and store in data1
    if microbit.button_a.is_pressed() == 1 and microbit.button_b.is_pressed() == 0:
        data1 = "a"
    elif microbit.button_a.is_pressed() == 0 and microbit.button_b.is_pressed() == 1:
        data1 = "b"
    elif microbit.button_a.is_pressed() == 1 and microbit.button_b.is_pressed() == 1 and mode_time.check():
        data1 = "0"
        mode += 1
        if mode > 3:
            mode = 0
    else:
        data1 = "0"
    data = data0 + data1 + str(mode) # put data0 and data1 together and store in data
    radio.send(data) # Send data