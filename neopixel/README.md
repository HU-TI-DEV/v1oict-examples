# V1OICT examples: NeoPixel

## Troubleshooting

> Ik wil mijn NeoPixel met een kleur laten oplichten, maar hij toont alleen wit! Wat kan ik doen?

Dit kan een gevolg zijn van onjuist timing in de communicatie tussen PICO en NeoPixel.

Bijvoorbeeld de "High Density Neopixel E497587" toont dit probleem.

Gelukkigerwijs kan dit makkelijk worden opgelost.

Als jij in een programma deze lijn schrijf:

```np = NeopPixel(Pin(13), 8)```

dan vertaald de [MicroPython NeoPixel library](https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/led/neopixel/neopixel.py) dit intern in een lijn met deze parameters:

```np = NeoPixel(Pin(13), 8, bpp=3, timing=(400, 850, 800, 450))```

Volgens het [WS2812 datasheet](https://www.alldatasheet.com/datasheet-pdf/download/553088/ETC2/WS2812.html) zijn deze instellingen voor het timing juist:

```np = NeoPixel(Pin(13), 8, bpp=3, timing=(350, 700, 800, 600))```

De parameter ```bpp=3``` kan je weglaten, dus kan je deze lijn gebruiken:

```np = NeoPixel(Pin(13), 8, timing=(350, 700, 800, 600))```

