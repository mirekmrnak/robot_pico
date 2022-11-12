from machine import Pin, PWM
import time, _thread
import motors, sensors, timer, servomotor

#Set up led pin
led = PWM(Pin(25))
led.freq(1000)

#Global variables
search_distance = []
second_threat_busy = False

def obstacle():
    return sensors.obstacles()[0] == 0 or sensors.obstacles()[1] == 0 or sensors.distance() < 30

def drive_search():
    global search_distance, second_threat_busy

    servomotor.set_position(-45)
    time.sleep(0.3)
    search_distance.append(sensors.distance())
    time.sleep(0.1)
    servomotor.set_position(45)
    time.sleep(0.3)
    search_distance.append(sensors.distance())
    time.sleep(0.1)
    second_threat_busy = False

def stop_search():
    global search_distance, second_threat_busy

    servomotor.set_position(-90)
    time.sleep(0.3)
    search_distance.append(sensors.distance())
    time.sleep(0.1)
    servomotor.set_position(90)
    time.sleep(0.3)
    search_distance.append(sensors.distance())
    time.sleep(0.1)
    second_threat_busy = False
    
def thread(function):
    global second_threat_busy
    if second_threat_busy == False:
        second_threat_busy = True
        second_thread = _thread.start_new_thread(function, ())
    else:
        pass

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
    longitudinal_ac = income["aceleration_x"] - 49
    #lateral acceleraion movement -> right, left
    lateral_ac = income["aceleration_y"] - 49
    
    #Mode 1; forward or backward with turning
    if income["button"] == "0":
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
            motors.carDrive(-longitudinal_sp, max(round(-longitudinal_sp + lateral_sp * turning_constant, 1), 0), max(round(-longitudinal_sp + lateral_sp * turning_constant, 1), 0), -longitudinal_sp)

        # Forward and turn right
        elif -longitudinal_deadzone > longitudinal_ac and lateral_ac > lateral_deadzone:
            longitudinal_sp = longitudinal_ac + longitudinal_deadzone
            lateral_sp = lateral_ac - lateral_deadzone
            motors.carDrive(max(round(-longitudinal_sp - lateral_sp * turning_constant, 1), 0), -longitudinal_sp, -longitudinal_sp, max(round(-longitudinal_sp  - lateral_sp * turning_constant, 1), 0))

        # Backward and turn left
        elif longitudinal_ac > longitudinal_deadzone and lateral_ac < -lateral_deadzone:
            longitudinal_sp = longitudinal_ac - longitudinal_deadzone
            lateral_sp = lateral_ac + lateral_deadzone
            motors.carDrive(-longitudinal_sp, min(round(-longitudinal_sp - lateral_sp * turning_constant, 1), 0), min(round(-longitudinal_sp - lateral_sp * turning_constant, 1), 0), -longitudinal_sp)

        # Backward and turn right
        elif longitudinal_ac > longitudinal_deadzone and lateral_ac > lateral_deadzone:
            longitudinal_sp = longitudinal_ac - longitudinal_deadzone
            lateral_sp = lateral_ac - lateral_deadzone
            motors.carDrive(min(round(-longitudinal_sp + lateral_sp * turning_constant, 1), 0), -longitudinal_sp, -longitudinal_sp, min(round(-longitudinal_sp  + lateral_sp * turning_constant, 1), 0))
        
        else:
            motors.carStop()

    elif income["button"] == "b":
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
    """
    Full automatic. Drives forward until obstacle is detected -> looks where is space and turn that way -> driwes forward
    """

    #timer_sensor_look = timer.Timer(0.25)

    speed = 40

    if obstacle():
        #Close obstacle behavior: find where is space and drive there
        
        motors.carStop()
        thread(stop_search) 

        # if search_distance:
        #         if search_distance[0] > search_distance[1]:
        #             motors.carDrive(-speed, speed, speed, -speed)
        #             search_distance.clear()
        #         else:
        #             motors.carDrive(speed, -speed, -speed, speed)
        #             search_distance.clear()

    else:
        if 30 < sensors.distance() < 120:
            #Try to avoid obstacle finding the space and driving around
            speed = 20

            motors.carDrive (speed, speed, speed, speed)
            thread(drive_search)

            # if search_distance:
            #     if search_distance[0] > search_distance[1]:
            #         motors.carDrive(speed / 2, speed, speed, speed / 2)
            #         search_distance.clear()
            #     else:
            #         motors.carDrive(-speed, speed / 2, speed / 2, -speed)
            #         search_distance.clear()

        else:
            #If path is clear drive forward
            #time.sleep(0.2)
            motors.carDrive (speed, speed, speed, speed)

def mode3():
    """
    Automatic line follow mode
    carDriveFunction(BR, BL, FL, FR) to control all motors
    BL - back_left, BR - back_right, FL - fornt_left, FR - front_right
    Input - int between -40 and +40 for each motor ->  + forward, - back, -right, +left; number sets up speed
    """
    speed = 5

    led.duty_u16(65025)  # just the light for

    where_is_line = sensors.linesensors()
    # returns list, where 1st - left sensor, 2nd - middle sensor, 3nd - right sensor
    # values: 1 - free, 0 - is line
    left = 0
    right = 0
    if where_is_line[0] == 1 and where_is_line[1] == 0 and where_is_line[2] == 1:
        motors.carDrive(speed, speed, speed, speed)
        # line is in middle - goes forward
    if where_is_line[0] == 0 and where_is_line[1] == 0 and where_is_line[2] == 1:
        motors.carDrive(speed/2, speed, speed, speed/2)
        # line is left and middle - goes slightly left
    if where_is_line[0] == 1 and where_is_line[1] == 0 and where_is_line[2] == 0:
        motors.carDrive(speed, speed/2, speed/2, speed)
        # line is middle and right - goes slightly right
    if where_is_line[0] == 0 and where_is_line[1] == 1 and where_is_line[2] == 1:
        motors.carDrive(speed, 0, 0, speed)
        # line is left goes left
        left = 0
        # line was at left before lost
    if where_is_line[0] == 1 and where_is_line[1] == 1 and where_is_line[2] == 1 and left == 0:
        motors.carDrive(speed, 0, 0, speed)
        # line lost at left goes left
    if where_is_line[0] == 1 and where_is_line[1] == 1 and where_is_line[2] == 0:
        motors.carDrive(0, speed, speed, 0)
        # line is right goes right
        right = 0
        # line was at right before lost
    if where_is_line[0] == 1 and where_is_line[1] == 1 and where_is_line[2] == 1 and right == 0:
        motors.carDrive( 0, speed, speed, 0)
        # line lost right goes right