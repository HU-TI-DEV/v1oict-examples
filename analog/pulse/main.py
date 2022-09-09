from machine import ADC, PWM, Pin
import time

led = Pin(20, Pin.OUT)
adc = ADC(Pin(26))


def pulse(pin, high_time, low_time):
    """
    Geef een puls op de pin:
    Maak de pin pin_nr hoog, wacht high_time,
    maak de pin laag, en wacht nog low_time
    """

    # implementeer deze functie


while True:
    adc_value = adc.read_u16()
    time.sleep(0.01)
