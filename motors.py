from machine import Pin, PWM

FREQ = 100 #FREQ for PWM control
U16 = 65535

# definice motoru
motor1 = Pin(4, Pin.OUT)
motor1b = Pin(5, Pin.OUT)
motor2 = Pin(2, Pin.OUT)
motor2b = Pin(3, Pin.OUT)

motor3 = Pin(12, Pin.OUT)
motor3b = Pin(13, Pin.OUT)
motor4 = Pin(14, Pin.OUT)
motor4b = Pin(15, Pin.OUT)

motors_forward = [motor1, motor2, motor3, motor4]
motors_backward = [motor1b, motor2b, motor3b, motor4b]

# nastavení hodnot všech motorů na log 0
for motor in motors_forward + motors_backward:
    motor.value(0)

def carDrive(BR, BL, FL, FR):
    '''
    Function to control all motors
    BL - back_left, BR - back_right, FL - fornt_left, FR - front_right
    Input - number between -1 and +1 for each motor
    '''
    for i, wheel in enumerate((BR, BL, FL, FR)):
        if 1 >= wheel > 0:
            motors_forward[i].value(1)
            motors_backward[i].value(0)
            #motors_forward[i].duty_u16(int(wheel*U16))
            #motors_backward[i].duty_u16(0)
        elif 0 > wheel >= -1:
            motors_forward[i].value(0)
            motors_backward[i].value(1)
        else:
            motors_forward[i].value(0)
            motors_backward[i].value(0)

def carStop():
    carDrive(0, 0, 0, 0)