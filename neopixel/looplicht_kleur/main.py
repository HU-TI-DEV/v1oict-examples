# NeoPixel looplicht_kleur
from machine import Pin
from time import sleep_ms
from neopixel import NeoPixel

np = NeoPixel(Pin(13), 8)

while True:
    sleep_ms(1000)
