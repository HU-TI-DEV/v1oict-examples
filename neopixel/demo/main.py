# v1oict-examples: NeoPixel demo/test code
from machine import Pin
from time import sleep_ms
from neopixel import NeoPixel

NEOPIX_PIN = Pin(13)
NEOPIX_LEN = 8

# High Density Neopixel E497587 heeft nog een parameter nodig:
np = NeoPixel(NEOPIX_PIN, NEOPIX_LEN, timing=(350, 700, 800, 600))
# WS2812B-8 werkt ook met de MicroPython standaard:
# np = NeoPixel(NEOPIX_PIN, NEOPIX_LEN)

while True:
    np[0] = [255, 0, 0]
    np[1] = [0, 255, 0]
    np[2] = [0, 0, 255]
    np.write()
    sleep_ms(1000)
    np[0] = [20, 0, 0]
    np[1] = [0, 20, 0]
    np[2] = [0, 0, 20]
    np.write()
    sleep_ms(1000)
