from machine import Pin, PWM

servo = PWM(Pin(8))
servo.freq(50)

def zero_position():
    """
    Sets servo position to default (forward)
    """
    servo.duty_u16(4875)

def set_position(position_angle):
    """
    Sets position of motor position angle = set position of motor [deg] (min = -90, max = 90)
    """
    duty = int(4875 + position_angle * 34.7222)
    servo.duty_u16(duty)

