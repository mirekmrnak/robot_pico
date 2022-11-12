from machine import Pin, PWM

# FREQ = 100 #FREQ for PWM control
# U16 = 65535

# constants
motor_dutyu16_min = int(25000)
motor_dutyu16_max = int(65000)

# definice motoru
motor1 = Pin(4, Pin.OUT)
motor1b = Pin(5, Pin.OUT)
motor2 = Pin(2, Pin.OUT)
motor2b = Pin(3, Pin.OUT)

motor3 = Pin(12, Pin.OUT)
motor3b = Pin(13, Pin.OUT)
motor4 = Pin(14, Pin.OUT)
motor4b = Pin(15, Pin.OUT)

motor1_speed = PWM(Pin(7))
motor1_speed.freq(100)
motor2_speed = PWM(Pin(6))
motor2_speed.freq(100)
motor3_speed = PWM(Pin(10))
motor3_speed.freq(100)
motor4_speed = PWM(Pin(11))
motor4_speed.freq(100)

motors_forward = [motor1, motor2, motor3, motor4]
motors_backward = [motor1b, motor2b, motor3b, motor4b]
motors_speed = [motor1_speed, motor2_speed, motor3_speed, motor4_speed]

# nastavení hodnot všech motorů na log 0
for motor in motors_forward + motors_backward:
    motor.value(0)

def round_step(number, step):
    """
    Rounds number to selected step -> number = 23, step = 5 => 25
    """
    return step * round(number / step)

def carDrive(BR, BL, FL, FR):
    '''
    Function to control all motors
    BL - back_left, BR - back_right, FL - fornt_left, FR - front_right
    Input - int between -40 and +40 for each motor ->  + forward, - back, -right, +left; number sets up speed
    '''
    for i, wheel in enumerate((BR, BL, FL, FR)):
        if wheel > 0:
            #Calculates duty step based on diffrence max - min, step of input signal - 40 and lower needed tilt of controler
            duty_step_coeficient = int(((motor_dutyu16_max - motor_dutyu16_min) / 40) * 1.5)
            motors_forward[i].value(1)
            motors_backward[i].value(0)
            wheel_speed = abs(round_step(int(wheel), 5))
            #print(max(min(motor_dutyu16_max, wheel_speed * duty_step_coeficient + motor_dutyu16_min), motor_dutyu16_min))
            motors_speed[i].duty_u16(max(min(motor_dutyu16_max, wheel_speed * duty_step_coeficient + motor_dutyu16_min), motor_dutyu16_min))

        elif 0 > wheel:
            #Calculates duty step based on diffrence max - min and step of input signal - 40
            duty_step_coeficient = int(((motor_dutyu16_max - motor_dutyu16_min) / 40 ) * 1.5)
            motors_forward[i].value(0)
            motors_backward[i].value(1)
            wheel_speed = abs(round_step(int(wheel), 5))
            #print(max(min(motor_dutyu16_max, wheel_speed * duty_step_coeficient + motor_dutyu16_min), motor_dutyu16_min))
            motors_speed[i].duty_u16(max(min(motor_dutyu16_max, wheel_speed * duty_step_coeficient + motor_dutyu16_min), motor_dutyu16_min))
        else:
            motors_forward[i].value(0)
            motors_backward[i].value(0)

def carStop():
    carDrive(0, 0, 0, 0)