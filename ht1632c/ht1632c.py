"""
Summary from the datasheet:

Holtek HT1632C 32x8 & 24x16 LED Driver

Features

 - Operating voltage: 2.4V~5.5V
 - Multiple LED display - 32 out bits/8 commons and 24 out bits/16 commons
 - Integrated display RAM - 64x4 (32/8) or 96x4 (24/16)
 - 16-level PWM brightness control
 - Integrated 256kHz RC oscillator
 - Serial MCU interface - _CS, _RD, _WR, DATA
 - Data mode & command mode instruction
 - Cascading function for extended applications
 - Selectable NMOS open drain output driver and PMOS open drain output driver for commons

General Description

 - The HT1632C is a memory mapping LED display controller/driver, which can select a number of ROW and commons.
 - These are 32 ROW & 8 commons and 24 ROW & 16 commons.
 - The device supports 16-gradation LEDs for each out line using PWM control with software instructions.
 - A serial interface is conveniently provided for the command mode and data mode.
 - Only three or four lines are required for the interface between the host controller and the HT1632C.
 - The display can be extended by cascading the HT1632C for wider applications.


[...]

Datasheet: https://cdn-shop.adafruit.com/datasheets/ht1632cv120.pdf
Protocol description: https://www.lucadentella.it/en/2012/10/03/matrice-di-led-con-ht1632c-2/
GitHub link: https://github.com/lucadentella/LedMatrix
"""
# WORK IN PROGRESS
from machine import Pin
from time import sleep_us
from micropython import const
import framebuf

# mode commands (MSB first, 3 bit)
_HT1632C_CMD = const(0b100)
_HT1632C_WRITE = const(0b101)
_HT1632C_READ = const(0b110)

# HT1632C command codes (MSB first, 8 bit plus 1 bit don't care)
_SYS_DIS = const(0x00)  # power-on default
_SYS_ON = const(0x01)
_LED_OFF = const(0x02)  # power-on default
_LED_ON = const(0x03)
_BLINK_OFF = const(0x08)  # power-on default
_BLINK_ON = const(0x09)
_MODE_SLAVE = const(0x10)
_MODE_MASTER_RC = const(0x18)  # power-on default
_MODE_MASTER_EXT_CLK = const(0x1C)
_COM_OPT_N08 = const(0x20)  # power-on default
_COM_OPT_N16 = const(0x24)
_COM_OPT_P08 = const(0x28)
_COM_OPT_P16 = const(0x2C)
_PWM_DUTY_0 = const(0xA0)  # 1/16 duty
_PWM_DUTY_F = const(0xAF)  # 16/16 duty, power-on default

# Data r/w is via A6...A0 D0...D3  (11 bits, lsb first)
# Continuous sequential write is possible (starting with e.g. address 0)

# minimum init is therefore: _SYS_EN, _LED_ON
# full sequence is: _SYS_DIS, _COM_OPT_N08, _MODE_MASTER_RC, _SYS_ON, _LED_ON
# after that Write RAM Data // Update RAM Data

_DIGIT_0 = const(0x1)
_MATRIX_SIZE = const(8)


class HT1632C(framebuf.FrameBuffer):
    """
    Driver for HT3216C 32x8 LED matrix display

    On some matrices, the display is inverted (rotated 180°), in this case
    you can use `rotate_180=True` in the class constructor.
    """

    def __init__(self, width, height, data, wr, cs, rotate_180=False):
        # Pins setup
        self.dt = data
        self.wr = wr  # active-low
        self.cs = cs  # active-low
        self.cs.init(Pin.OUT, 1)
        self.wr.init(Pin.OUT, 1)
        self.dt.init(Pin.OUT, 0)
        # Dimensions
        self.width = width
        self.height = height
        # Guess matrices disposition
        self.cols = width // _MATRIX_SIZE
        self.rows = height // _MATRIX_SIZE
        self.nb_matrices = self.cols * self.rows
        self.rotate_180 = rotate_180
        # 1 bit per pixel (on / off) -> 8 bytes per matrix
        self.buffer = bytearray(width * height // 8)
        format = framebuf.MONO_HLSB if not self.rotate_180 else framebuf.MONO_HMSB
        super().__init__(self.buffer, width, height, format)
        # Init display
        self.init_display()

    def _send_bits_normal(self, bits, first_bit):
        """Send bits (msb first)"""
        self.cs(0)
        while first_bit:
            bit = 1 if bits & first_bit else 0
            self.dt(bit)
            self.wr(0)
            first_bit >>= 1
            self.wr(1)
        self.dt(0)
        self.cs(1)

    def _send_bits_debug(self, bits, first_bit):
        """Send bits (msb first)"""
        debug_string = ""
        self.cs(0)
        while first_bit:
            bit = 1 if bits & first_bit else 0
            debug_string += chr(48 + bit)
            self.dt(bit)
            self.wr(0)
            first_bit >>= 1
            self.wr(1)
        self.dt(0)
        self.cs(1)
        print(debug_string)

    _send_bits = _send_bits_normal

    def _write_command(self, command):
        """Send an 8-bit command to the controller"""
        cmd = (_HT1632C_CMD << 9) | (command << 1) | 0
        self._send_bits(cmd, 1 << 11)

    def _write_data(self, address, data):
        swap = [0b0000, 0b1000, 0b0100, 0b1100,
                0b0010, 0b1010, 0b0110, 0b1110,
                0b0001, 0b1001, 0b0101, 0b1101,
                0b0011, 0b1011, 0b0111, 0b1111]
        """Send a 3-bit write mode, a 7-bit address, and a succession of 8-bit data values"""
        cmd = (_HT1632C_WRITE << 7) | address
        fbi = 1 << 9
        bar = bytearray([data])
        i = 0
        while i < len(bar):
            byte = bar[i]
            i += 1
            cmd = (cmd << 8) | byte
            fbi <<= 8
        self._send_bits(cmd, fbi)

    def init_display(self):
        """Init hardware"""
        for command in (_SYS_DIS, _COM_OPT_N08, _MODE_MASTER_RC, _SYS_ON, _LED_ON):
            self._write_command(command)
        self.fill(0)
        self.show()

    def brightness(self, value):
        """Set display brightness (0 to 15)"""
        if not 0 <= value < 16:
            raise ValueError("Brightness must be between 0 and 15")
        self._write_command(_PWM_DUTY_0 | value)

    def show(self):
        """Update display"""
        ramidx = 62
        for matrix in range(self.nb_matrices):
            for line in range(8):
                # Guess where the matrix is placed
                row, col = divmod(matrix, self.cols)
                # Compute where the data starts
                if self.rotate_180:
                    offset = (self.rows - row) * self.cols * 8 - 1
                    index = offset - self.cols * line - col
                else:
                    offset = row * self.cols * 8
                    index = offset + self.cols * line + col
                # Write data to the matrix display
                # print('ramidx =', ramidx, ' line = ', line, ' matrix = ', matrix)
                self._write_data(ramidx, self.buffer[index])
                ramidx -= 2

# eof
