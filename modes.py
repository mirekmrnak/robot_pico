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
    #Constants
    longitudinal_deadzone = 10
    lateral_deadzone = 10
    turning_constant = 0.9

    led.duty_u16(int(65025 * 0.25))    

    #longitudinal acceleration -> forward, backward
    longitudinal_ac = int(income[0] + income[1]) - 49
    #lateral acceleraion movement -> right, left
    lateral_ac = int(income[2] + income[3]) - 49
    

    #Mode 1; forward or backward with turning
    if income[4] == "0":
        # Forward 
        if -longitudinal_deadzone > longitudinal_ac and (-lateral_deadzone <= lateral_ac <= lateral_deadzone):
            longitudinal_sp = longitudinal_ac + longitudinal_deadzone
            motors.carDrive(-longitudinal_sp, -longitudinal_sp, -longitudinal_sp, -longitudinal_sp)
        
        # Backward
        elif longitudinal_ac > longitudinal_deadzone and (-lateral_deadzone <= lateral_ac <= lateral_deadzone):
            longitudinal_sp = longitudinal_ac - longitudinal_deadzone
            motors.carDrive(-longitudinal_sp, -longitudinal_sp, -longitudinal_sp, -longitudinal_sp)
        
        # Left on spot
        elif (-longitudinal_deadzone <= longitudinal_ac <= longitudinal_deadzone) and -lateral_deadzone > lateral_ac:
            lateral_sp = lateral_ac + lateral_deadzone
            motors.carDrive(-lateral_sp, lateral_sp, lateral_sp, -lateral_sp)
        
        # Right on spot
        elif (-longitudinal_deadzone <= longitudinal_ac <= longitudinal_deadzone) and lateral_deadzone < lateral_ac:
            lateral_sp = lateral_ac - lateral_deadzone
            motors.carDrive(-lateral_sp, lateral_sp, lateral_sp, -lateral_sp)

        # Forward and turn left
        elif -longitudinal_deadzone > longitudinal_ac and lateral_ac < -lateral_deadzone:
            longitudinal_sp = longitudinal_ac + longitudinal_deadzone
            lateral_sp = lateral_ac + lateral_deadzone
            motors.carDrive(-longitudinal_sp, round(-longitudinal_sp + lateral_sp * turning_constant, 1), round(-longitudinal_sp + lateral_sp * turning_constant, 1), -longitudinal_sp)

        # Forward and turn right
        elif -longitudinal_deadzone > longitudinal_ac and lateral_ac > lateral_deadzone:
            longitudinal_sp = longitudinal_ac + longitudinal_deadzone
            lateral_sp = lateral_ac - lateral_deadzone
            motors.carDrive(round(-longitudinal_sp - lateral_sp * turning_constant, 1), -longitudinal_sp, -longitudinal_sp, round(-longitudinal_sp  - lateral_sp * turning_constant, 1))

        # # Backward and turn left
        elif longitudinal_ac > longitudinal_deadzone and lateral_ac < -lateral_deadzone:
            longitudinal_sp = longitudinal_ac - longitudinal_deadzone
            lateral_sp = lateral_ac + lateral_deadzone
            motors.carDrive(-longitudinal_sp, round(-longitudinal_sp - lateral_sp * turning_constant, 1), round(-longitudinal_sp - lateral_sp * turning_constant, 1), -longitudinal_sp)

        # Backward and turn right
        elif longitudinal_ac > longitudinal_deadzone and lateral_ac > lateral_deadzone:
            longitudinal_sp = longitudinal_ac - longitudinal_deadzone
            lateral_sp = lateral_ac - lateral_deadzone
            motors.carDrive(round(-longitudinal_sp + lateral_sp * turning_constant, 1), -longitudinal_sp, -longitudinal_sp, round(-longitudinal_sp  + lateral_sp * turning_constant, 1))
        
        else:
            motors.carStop()

    elif income[4] == "b":
        #Right g-turn (tank turn)
        if -lateral_deadzone > lateral_ac:
            lateral_sp = lateral_ac + lateral_deadzone
            motors.carDrive(lateral_sp, -lateral_sp, lateral_sp, -lateral_sp)

        #Right g-turn (tank turn)
        elif lateral_deadzone < lateral_ac:
            lateral_sp = lateral_ac - lateral_deadzone
            motors.carDrive(lateral_sp, -lateral_sp, lateral_sp, -lateral_sp)

        else:
            motors.carStop()

    else:
        motors.carStop()        
        
def mode2(income):
    speed_preset = [10, 25, 40]
    n = 2
    speed = speed_preset[n]
    #if income[4] == "b":
        #speed = speed_preset[n + 1]
        
    led.duty_u16(int(65025 * 0.3))
    
    if obstacle():
        motors.carStop()
        sleep(2)
        print(speed)
        motors.carDrive(-speed, speed, speed, -speed)
        sleep(2)
    
    motors.carDrive(speed, speed, speed, speed)


def mode3():
    led.duty_u16(65025)
    motors.carStop()