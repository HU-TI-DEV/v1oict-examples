import time

from machine import SPI, Pin

from max7219 import Max7219

spi = SPI(1, baudrate=10000000, sck=Pin(10), mosi=Pin(11))
screen = Max7219(8, 8, spi, Pin(13))

while True:
    for x in range(48, 122):
        screen.fill(0)
        screen.text(chr(x), 0, 0, 1)
        screen.show()
        time.sleep(1)
