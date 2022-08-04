
# rsdoa.py
# using tuning.py to get doa (respeaker based)

from tuning import Tuning
import usb.core
import usb.util
import time

# dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

dev = usb.core.find(idVendor=0x0d8c, idProduct=0x0014)

if dev:
    Mic_tuning = Tuning(dev)
    print (Mic_tuning.direction)
    while True:
        try:
            print(Mic_tuning.direction)
            time.sleep(1)
        except KeyboardInterrupt:
            break
    # print("here")
