from machine import Pin
import time

led_pin = Pin(0, Pin.OUT)

trigger_pin = Pin(14, Pin.OUT)
echo_pin = Pin(15, Pin.IN)

while True:
    trigger_pin.value(1)
    time.sleep_us(10)
    trigger_pin.value(0)

    for i in range(0, 100):
        if echo_pin.value():
            led_pin.value(1)
            time.sleep_ms(1000)
            break
        time.sleep_ms(1)

    led_pin.value(0)
