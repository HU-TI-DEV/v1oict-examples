from machine import Pin
import time

gpio_pin = Pin(20, Pin.OUT)


def pulse(pin, high_time, low_time):
    """
    Geef een puls op de pin:
    Maak de pin pin_nr hoog, wacht high_time,
    maak de pin laag, en wacht nog low_time
    """

    # Kopier hier je pulse implementatie


def morse(pin, dot_length, text):
    """
    Laat de text horen als morse code.
    De pin_nr is de pin die gebruikt wordt.
    De text mag de volgende characters bevatten: spatie, streepje, punt.
    De dot_length is de lengte van een punt (dot).
    De lengte van de andere characters wordt daar van afgeleid.
    """

    # Kopier hier je morse implementatie


def morse_text(pin, dot_length, text):
    """
    Laat de string s horen als morse code.
    De pin_nr is de pin die gebruikt wordt.
    De text mag de volgende characters bevatten: lowercase letters, spatie.
    De dot_length is de lengte van een punt (dot).
    De lengte van de andere characters wordt daar van afgeleid.
    """

    # implementeer deze functie


morse_text(gpio_pin, 0.2, "Hello world")
