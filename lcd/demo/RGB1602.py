# -*- coding: utf-8 -*-
import time
from machine import Pin, I2C

RGB1602_SDA = Pin(4)
RGB1602_SCL = Pin(5)

# RGB1602_I2C = I2C(0, sda=RGB1602_SDA, scl=RGB1602_SCL, freq=400000)
RGB1602_I2C = I2C(0, sda=RGB1602_SDA, scl=RGB1602_SCL, freq=125000)

# Device I2C Address
LCD_ADDRESS = (0x7C >> 1)
RGB_ADDRESS = (0xC0 >> 1)
# for LCD1602 RGB module, I2C.Scan() shows another (unknown) I2C device
# UNK_ADDRESS = (0xE0 >> 1)

# RGB color definitions
REG_RED = 0x04
REG_GREEN = 0x03
REG_BLUE = 0x02
REG_MODE1 = 0x00
REG_MODE2 = 0x01
REG_OUTPUT = 0x08

# LCD commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# Entry Mode flags
LCD_ENTRYRTL = 0x00  # Right-to-Left
LCD_ENTRYLTR = 0x02  # Left-to-Right
LCD_ENTRYSHIFT = 0x01
LCD_ENTRYNOSHIFT = 0x00

# Display Control flags
LCD_DISPLAYON = 0x04
LCD_CURSORON = 0x02
LCD_BLINKON = 0x01
LCD_DISPLAYOFF = 0x00
LCD_CURSOROFF = 0x00
LCD_BLINKOFF = 0x00

# Display/Cursor Shift flags
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# Function Set flags
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x8DOTS = 0x00


class RGB1602:
    def __init__(self, columns=16, rows=2):
        self._cols = columns
        self._rows = rows
        self._showfunction = LCD_FUNCTIONSET | LCD_4BITMODE | LCD_5x8DOTS
        self._showfunction |= (LCD_1LINE if rows < 2 else LCD_2LINE)
        self._showcontrol = LCD_DISPLAYCONTROL | LCD_CURSOROFF | LCD_BLINKOFF
        self.begin()

    def command(self, cmd):
        RGB1602_I2C.writeto(LCD_ADDRESS, bytearray([0x80, cmd]))

    def write(self, data):
        RGB1602_I2C.writeto(LCD_ADDRESS, bytearray([0x40, data]))

    def printout(self, arg):
        if isinstance(arg, int):
            arg = str(arg)
        # bytearray(arg, 'utf-8') will make two characters from arg string/chr values 128..255
        # x=0..127: [x], x=128..191: [0xC2, x], 192..255: [0xC3, x - 64]
        # bytearray(arg, 'latin-1') preserves x for all chr(x) values from 0..255
        # x=0..255: [x]
        # RGB1602_I2C.writeto_mem(LCD_ADDRESS, 0x40, bytearray(arg, 'utf-8'))
        RGB1602_I2C.writeto_mem(LCD_ADDRESS, 0x40, bytearray(arg, 'latin-1'))
        return self  # enable command chaining

    def set_reg(self, reg, data):
        RGB1602_I2C.writeto(RGB_ADDRESS, bytearray([reg, data]))

    def begin(self):
        # wait for more than 15 ms after VDD rises to 4.5V
        time.sleep(0.050)
        self.command(self._showfunction)
        time.sleep(0.005)
        self.command(self._showfunction)
        time.sleep(0.005)
        self.command(self._showfunction)
        # 4th try
        self.command(self._showfunction)
        # turn the display on with no cursor or blinking default
        self.display()
        # clear it
        self.clear()
        # Initialize to default text direction (for roman languages)
        self.command(LCD_ENTRYMODESET | LCD_ENTRYLTR | LCD_ENTRYNOSHIFT)
        # RGB backlight init
        self.set_reg(REG_MODE1, 0)
        # set LEDs controllable by both PWM and GRPPWM registers
        self.set_reg(REG_OUTPUT, 0xFF)
        # set MODE2 values
        # 0b0010_0000 -> 0x20  (DMBLNK to 1, ie blinky mode)
        self.set_reg(REG_MODE2, 0x20)
        self.set_color_white()
        return self  # enable command chaining

    def at(self, col, row):
        col |= (0x80 if row < 1 else 0xC0)
        self.command(col)
        return self  # enable command chaining

    def clear(self):
        self.command(LCD_CLEARDISPLAY)
        time.sleep(0.002)
        return self  # enable command chaining

    def home(self):
        self.command(LCD_RETURNHOME)
        time.sleep(0.002)
        return self  # enable command chaining

    def display(self, on=True):
        self.command(self._showcontrol | (LCD_DISPLAYON if on else LCD_DISPLAYOFF))
        return self  # enable command chaining

    def set_rgb(self, r, g, b):
        self.set_reg(REG_RED, r)
        self.set_reg(REG_GREEN, g)
        self.set_reg(REG_BLUE, b)
        return self  # enable command chaining

    def set_color_white(self):
        self.set_rgb(255, 255, 255)
        return self  # enable command chaining
