import RGB1602

lcd = RGB1602.RGB1602(16, 2)

while True:
    lcd.printout("Welkom studenten")
    lcd.setCursor(0, 1)
    lcd.printout("HBO-ICT 2022 ")
