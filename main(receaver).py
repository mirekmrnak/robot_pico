from microbit import sleep, button_a, button_b, display, uart
from microbit import Image, pin0, pin1
import radio

sleep(500)
display.show(Image.ALL_CLOCKS, loop=False, delay=100)
sleep(500)

uart.init(baudrate=9600, bits=8, tx=pin0, rx=pin1)
radio.on()

while True:
    incoming = radio.receive() # Reception via radio hardware is stored in the incoming variable

    if incoming != None: # if incoming is not None (empty) then:
        display.show(Image.YES, loop=False)
        #display.show(Image.ALL_CLOCKS, loop=False, delay=60)
        transfer = 'X' + incoming + 'X' + incoming
        uart.write(transfer)
        
    else: # if incoming = None, then the Joy-Car is parked.
        # This usually happens when the Joy-Car is out of range of the remote control or when the remote control is off.
        display.show(Image.NO, loop=False)
        uart.write('X000000X000000')