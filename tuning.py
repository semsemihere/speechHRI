# tuning.py
# tuning class
# dragged from ReSpeaker files

from array import array
import sys
import struct
import usb.core
import usb.util


USAGE = """Usage: python {} -h
        -p      show all parameters
        -r      read all parameters
        NAME    get the parameter with the NAME
        NAME VALUE  set the parameter with the NAME and the VALUE
"""



# parameter list
# name: (id, offset, type, max, min , r/w, info)
PARAMETERS = {
    'SPEECHDETECTED': (19, 22, 'int', 1, 0, 'ro', 'Speech detection status.', '0 = false (no speech detected)', '1 = true (speech detected)'),
    'VOICEACTIVITY': (19, 32, 'int', 1, 0, 'ro', 'VAD voice activity status.', '0 = false (no voice activity)', '1 = true (voice activity)'),
    'GAMMAVAD_SR': (19, 39, 'float', 1000, 0, 'rw', 'Set the threshold for voice activity detection.', '[-inf .. 60] dB (default: 3.5dB 20log10(1.5))'),
    # 'KEYWORDDETECT': (20, 0, 'int', 1, 0, 'ro', 'Keyword detected. Current value so needs polling.'),
    'DOAANGLE': (21, 0, 'int', 359, 0, 'ro', 'DOA angle. Current value. Orientation depends on build configuration.')
}






class Tuning:
    TIMEOUT = 100000

    def __init__(self, dev):
        self.dev = dev

    def write(self, name, value):
        try:
            data = PARAMETERS[name]
        except KeyError:
            return

        if data[5] == 'ro':
            raise ValueError('{} is read-only'.format(name))

        id = data[0]

        # 4 bytes offset, 4 bytes value, 4 bytes type
        if data[2] == 'int':
            payload = struct.pack(b'iii', data[1], int(value), 1)
        else:
            payload = struct.pack(b'ifi', data[1], float(value), 0)

        self.dev.ctrl_transfer(
            usb.util.CTRL_OUT | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
            0, 0, id, payload, self.TIMEOUT)

    def read(self, name):
        try:
            data = PARAMETERS[name]
        except KeyError:
            return

        id = data[0]

        cmd = 0x80 | data[1]
        if data[2] == 'int':
            cmd |= 0x40

        length = 8
        

        # print("---------------------------")
        
        # print (usb.util.CTRL_IN) #128
        # print (usb.util.CTRL_TYPE_VENDOR) #64
        # print (usb.util.CTRL_RECIPIENT_DEVICE) #0

        # print (usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE) #192
        # print (cmd) #192
        # print (id) #21
        # print (length) #8
        # print (self.TIMEOUT) #100000

        # print (type(usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE))
        # print (type(cmd))
        # print (type(id) )
        # print (type(length)) 
        # print (type(self.TIMEOUT))
        
        # print("---------------------------")



        # response = self.dev.ctrl_transfer(usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE, 0, cmd, id, length, self.TIMEOUT)
        
        response = self.dev.ctrl_transfer(192, 0, 192, 21, 8, 100000)
        print("response: ", response)


        response = struct.unpack(b'ii', response.tostring())
        print("response: ", response)
	

        if data[2] == 'int':
            result = response[0]
        else:
            result = response[0] * (2.**response[1])

        return result

    def set_vad_threshold(self, db):
        self.write('GAMMAVAD_SR', db)

    def is_voice(self):
        return self.read('VOICEACTIVITY')

    @property
    def direction(self):
        return self.read('DOAANGLE')

    @property
    def version(self):
        return self.dev.ctrl_transfer(
            usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
            0, 0x80, 0, 1, self.TIMEOUT)[0]

    def close(self):
        """
        close the interface
        """
        usb.util.dispose_resources(self.dev)

# def find(vid=0x2886, pid=0x0018): 
# 0d8c:0014 for audist
def find(vid=0x0d8c, pid=0x0014):
    dev = usb.core.find(idVendor=vid, idProduct=pid)
    if not dev:
        print("Not Found")
        return

    configuration = dev.get_active_configuration()

    interface_number = None
    for interface in configuration:
        interface_number = interface.bInterfaceNumber

        if dev.is_kernel_driver_active(interface_number):
            dev.detach_kernel_driver(interface_number)

    return Tuning(dev)



def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '-p':
            print('name\t\t\ttype\tmax\tmin\tr/w\tinfo')
            print('-------------------------------')
            for name in sorted(PARAMETERS.keys()):
                data = PARAMETERS[name]
                print('{:16}\t{}'.format(name, '\t'.join([str(i) for i in data[2:7]])))
                for extra in data[7:]:
                    print('{}{}'.format(' '*60, extra))
        else:
            dev = find()
            if not dev:
                print('No device found')
                sys.exit(1)

            # print('version: {}'.format(dev.version))

            if sys.argv[1] == '-r':
                print('{:24} {}'.format('name', 'value'))
                print('-------------------------------')
                for name in sorted(PARAMETERS.keys()):
                    print('{:24} {}'.format(name, dev.read(name)))
            else:
                name = sys.argv[1].upper()
                if name in PARAMETERS:
                    if len(sys.argv) > 2:
                        dev.write(name, sys.argv[2])
                    
                    print('{}: {}'.format(name, dev.read(name)))
                else:
                    print('{} is not a valid name'.format(name))

            dev.close()
    else:
        print(USAGE.format(sys.argv[0]))

if __name__ == '__main__':
    main()