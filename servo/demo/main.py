from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(21))

pwm.freq(50)

while True:
    for duty in range(1000, 9000, 50):
        pwm.duty_u16(duty)
        sleep(0.01)
    for duty in range(9000, 1000, -50):
        pwm.duty_u16(duty)
        sleep(0.01)
