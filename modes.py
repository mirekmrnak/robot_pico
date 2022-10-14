from machine import Pin, PWM
from time import sleep
import motors
import sensors

#Set up led pin
led = PWM(Pin(25))
led.freq(1000)

def obstacle():
    return sensors.obstacles()[0] == '0' or sensors.obstacles()[1] == '0' or sensors.distance() < 30

def mode0():

    led.duty_u16(0)
    motors.carStop()

def mode1(income):
    """
    Remote controller mode.
    """

    led.duty_u16(int(65025 * 0.25))    
    speed = 0.5
    
    #move forward
    if income[0] == 'f':
        motors.carDrive(speed, speed, speed, speed)
    #move backward
    elif income[0] == 'b':
        motors.carDrive(-speed, -speed, -speed, -speed)
    #turn left
    elif income[0] == 'l':
        motors.carDrive(-speed, speed, speed, -speed)
    #turn right
    elif income[0] == 'r':
        motors.carDrive(speed, -speed, -speed, speed)
    #move left
    elif income[1] == 'a':
        motors.carDrive(-speed, speed, -speed, speed)
    #move right
    elif income[1] == 'b':
        motors.carDrive(speed, -speed, speed, -speed)
    else:
        motors.carStop()

def mode2():
    speed = 0.5
    led.duty_u16(int(65025 * 0.3))
    
    if obstacle():
        motors.carStop()
        sleep(2)
        motors.carDrive(-speed, speed, speed, -speed)
        sleep(2)
    
    motors.carDrive(speed, speed, speed, speed)


def mode3():
    led.duty_u16(65025)
    motors.carStop()