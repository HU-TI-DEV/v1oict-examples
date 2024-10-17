import machine
import utime

led = machine.Pin("LED", machine.Pin.OUT)

while True:
    led.toggle()  # Toggle the LED state
    utime.sleep(1)  # Wait for 1 second
