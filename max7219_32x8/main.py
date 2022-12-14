"""
Oriëntatie op TI

max7219 32x8 LED Matrix demo for Raspberry Pico and Pico W

(c) 2022 Hogeschool Utrecht,
Hagen Patzke (hagen.patzke@hu.nl)
"""

from machine import SPI, Pin
from max7219 import Max7219
from time import sleep_ms

# Hardware-dependent definitions --------------------------------------------

# SPI interface
spi_id = 1
spi_sck = Pin(10)
spi_mosi = Pin(11)
spi_cs = Pin(13)

# LED matrix dimensions
matrix_width = 32
matrix_height = 8

# Helper functions ----------------------------------------------------------

global builtin_led


def builtin_led_init():
    """ Init the built-in LED pin.
      On the Pico W, the built-in LED is not directly attached to a GPIO pin,
      but to the wireless chip. MicroPython encapsulates this with a named Pin "LED".
      Older versions of MicroPython don't know this, so we fall back to pin 25.
    """
    global builtin_led
    try:
        builtin_led = Pin("LED", Pin.OUT)
    except TypeError:
        builtin_led = Pin(25, Pin.OUT)


def builtin_led_blink():
    """ Flash the built-in LED for 200ms, then pause for 200ms. """
    global builtin_led
    builtin_led.value(1)
    sleep_ms(400)
    builtin_led.value(0)
    sleep_ms(400)


# main program --------------------------------------------------------------

""" 
  Make sure the hardware is reset _after_ we have stable power.
  For this, we blink the built-in LED three times between init steps.
  This adds a delay that gives the power source time to get up to the necessary voltage.
  The Pico will be fine from 1.8V, but the LED matrix needs a higher voltage to work.
  This delay is important if we want to use e.g. a power bank or wall adaptor.
"""

builtin_led_init()
builtin_led_blink()
# Init SPI port 1
spi = SPI(spi_id, baudrate=10000000, sck=spi_sck, mosi=spi_mosi)

builtin_led_blink()
# Init Max7219 matrix LED (width=32 if we have four 8x8 modules)
screen = Max7219(matrix_width, matrix_height, spi=spi, cs=spi_cs, rotate_180=False)

builtin_led_blink()
# It's demo time!
while True:
    for b in range(2):
        screen.brightness(b * 4)  # 4 is already bright, 15 is VERY bright
        # Show the characters from 32 to 126
        for x in range(32, 127):
            s = chr(x)
            if x < 100:
                s += ' :'[x & 1]  # same function as: s += ':' if x & 1 else ' '
            s += str(x)
            screen.fill(0)
            screen.text(s, 0, 0, 1)
            screen.show()
            sleep_ms(200)
        # Show the brightness levels from 0 to 15
        for sb in range(16):
            screen.brightness(sb)
            screen.fill(0)
            screen.text('B' + hex(sb), 0, 0, 1)
            screen.show()
            sleep_ms(1000)

# eof