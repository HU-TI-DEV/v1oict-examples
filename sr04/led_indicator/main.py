from machine import Pin
import time

led_pins = [
    Pin(0, Pin.OUT),
    Pin(1, Pin.OUT),
    Pin(2, Pin.OUT),
    Pin(3, Pin.OUT),
    Pin(4, Pin.OUT)
]

trigger_pin = Pin(14, Pin.OUT)
echo_pin = Pin(15, Pin.IN)


def measure_distance():
    """
        Meet de afstand met de SR04
    """

    # implementeer deze functie

    return 0


def display_distance(distance):
    """
        Laat de afstand d.m.v. de leds zien.
        1 led =  10 cm
        2 leds = 15 cm
        3 leds = 20 cm
        4 leds = 25 cm
        5 leds = 30 cm
    """

while True:
    distance = measure_distance()
    display_distance(distance)
    time.sleep_ms(100)
