from machine import Pin
import time

gpio_pin = Pin(20, Pin.OUT)

while True:
    gpio_pin.value(1)
    time.sleep(0.5)
    gpio_pin.value(0)
    time.sleep(0.5)
