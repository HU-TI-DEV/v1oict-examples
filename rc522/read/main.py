from rc522 import MFRC522
from os import uname
import time

reader = MFRC522(sck=10, mosi=11, miso=12, rst=14, cs=15, spi_id=1)

print("")
print("Please place card on reader")
print("")

try:
    while True:

        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                print("Card detected {}  uid={}".format(hex(int.from_bytes(bytes(uid), "little", False)).upper(),
                                                        reader.tohexstring(uid)))
                defaultKey = [255,255,255,255,255,255]
                reader.MFRC522_DumpClassic1K(uid, Start=0, End=64, keyA=defaultKey)
                print("Done")
            else:
                pass
        time.sleep(1)

except KeyboardInterrupt:
    pass




