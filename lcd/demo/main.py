import RGB1602
import time

"""
From the LCD1602 RGB Module datasheet:
Operating voltage: 3.3 ~ 5V,  LCD controller: AiP31068
Communication Interface: I2C, RGB driver:     PCA9633
Display Panel character LCD,  Display size: 64.5 × 16.0mm
Characters: 16 × 2, Dimensions: 87.0 × 32.0 × 13.0mm
Backlight colors: 16M, Operating temperature: -20 ~ +70℃
"""


def define_characters(lcd):
    heart = bytearray([0x00, 0x00, 0x1B, 0x1F, 0x1F, 0x0E, 0x04, 0x00])  # '@@[__ND@'
    face = bytearray([0x00, 0x00, 0x0A, 0x00, 0x11, 0x0E, 0x00, 0x00])  # '@@J@QN@@'
    lcd.command(0x40)  # custom char 0 at (0x40 | (0 << 3))
    lcd.printout(heart)
    lcd.command(0x48)  # custom char 1 at (0x40 | (1 << 3))
    lcd.printout(face)
    # Dirty trick:
    # Because the 5x7 matrix for display only uses bits 5,4,3,2,1
    # we can set bit 6 (0x40) and make the value a character
    # ASCII 0x40 = '@', 0x41 = 'A', ... , 0x5F = '_'
    lcd.command(0x50)  # custom char 2 at (0x40 | (2 << 3))
    lcd.printout('@@[__ND@')  # heart, alternative definition
    lcd.command(0x58)  # custom char 3 at (0x40 | (3 << 3))
    lcd.printout('@@J@QN@@')  # face, alternative definition


def show_r_g_b(lcd):
    lcd.set_rgb(255, 127, 127)
    time.sleep(1)
    lcd.set_rgb(127, 255, 127)
    time.sleep(1)
    lcd.set_rgb(127, 127, 255)
    time.sleep(1)
    lcd.set_rgb(255, 0, 0)
    time.sleep(1)
    lcd.set_rgb(0, 255, 0)
    time.sleep(1)
    lcd.set_rgb(0, 0, 255)
    time.sleep(1)


def discoloration(lcd):
    """
    Soft color change.

    Source: https://www.waveshare.com/wiki/Raspberry_Pi_Pico#LCD1602_I2C_Example
    """
    from math import pi, sin
    deg2rad = pi / 180
    t = 0
    while t < 360:
        r = int((abs(sin(deg2rad * t))) * 255)
        g = int((abs(sin(deg2rad * (t + 60)))) * 255)
        b = int((abs(sin(deg2rad * (t + 120)))) * 255)
        lcd.set_rgb(r, g, b)
        t = t + 3
        time.sleep(0.1)


def animated_banner(lcd):
    # First line
    target_pos = 1
    for char in "Welkom student":
        for ani in range(16, target_pos - 1, -1):
            lcd.at(ani, 0).printout(char)
            if (ani < 15):
                lcd.at(ani + 1, 0).printout(' ')
            time.sleep(0.1)
        target_pos += 1
    # Second line
    lcd.at(2, 1)
    for char in "HBO-ICT 2022":
        lcd.printout(char)
        time.sleep(0.1)


def fade(lcd, fade_in=True):
    for i in range(256):
        v = i if fade_in else 255 - i
        lcd.set_rgb(v, v, v)
        time.sleep(0.01)


def demo():
    """
    RGB1602 demonstration

    Modified 2022-10-13 by Hagen Patzke, Hogeschool Utrecht HBO-ICT TI
    """
    lcd = RGB1602.RGB1602(16, 2)

    define_characters(lcd)

    while True:
        lcd.clear()
        fade(lcd, fade_in=True)
        lcd.set_color_white()
        # The RGB1602 functions return 'self' -> we can chain commands (!)
        lcd.at(2, 0).printout(chr(0) + " WELCOME " + chr(1))
        lcd.at(3, 1).printout(chr(1) + " STUDENT " + chr(2))
        # "Discoloration" demo
        discoloration(lcd)
        # Display off for a moment
        lcd.display(False)
        time.sleep(1)
        lcd.set_color_white()
        lcd.display(True)
        # Show second banner
        lcd.clear()
        animated_banner(lcd)
        time.sleep(2)
        show_r_g_b(lcd)
        fade(lcd, fade_in=False)


if __name__ == '__main__':
    demo()
