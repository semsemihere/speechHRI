from tuning import Tuning
import usb.core
import usb.util
import time

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
#print dev
if dev:
    #print('1')
    Mic_tuning = Tuning(dev)
    #print('2')
    print(Mic_tuning.is_voice())
    #print('3') 

    while True:
        try:
            print(Mic_tuning.is_voice())
            time.sleep(1)
        except KeyboardInterrupt:
            break
