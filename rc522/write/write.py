from rc522 import MFRC522

'''
BE AWARE that sectors(3,7,11,15,...,63) are access block.
if you want to change  (sector % 4) == 3 you should
know how keys and permission work!
'''



def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring

reader = MFRC522(sck=10, mosi=11, miso=12, rst=14, cs=15, spi_id=1)

print("")
print("Please place card on reader")
print("")

key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

try:
    while True:

        (stat, tag_type) = reader.request(reader.REQIDL)

        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                print(uid)
                print("Card detected %s" % uidToString(uid))
                print("Test ! writing sector 2, block 0 (absolute block(8)")
                print("with TEST1234567890ABC")
                absoluteBlock=1
                value=[ord(x) for x in "TEST1234567890ABC"]
                status = reader.auth(reader.AUTHENT1A, absoluteBlock, key, uid)
                if status == reader.OK:
                    status = reader.write(absoluteBlock,value)
                    if status == reader.OK:
                        reader.MFRC522_DumpClassic1K(uid,keyA=key)
                    else:
                        print("unable to write")
                else:
                    print("Authentication error for writing")
                break
except KeyboardInterrupt:
    print("Bye")




