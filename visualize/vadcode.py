# Matlab plot of VAD

### library for matlab
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
### library for doa
from tuning import Tuning
import usb.core
import usb.util

### library for vad
import sounddevice as sd
import numpy as np
import copy
import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
cli = ("127.0.0.1", 9999)
data = b'True'

error_wave = ''

gijunjum = 1000

duration = 3  # seconds

prev_wave = []

titleFont = {
    'fontsize': 14,
    'fontweight': 'bold'
}

subFont = {
    'fontsize': 10,
    'fontweight': 'light'
}

# sound volume of each mics
volume = [0, 0, 0, 0, 0]
# mic = ["mic1","mic2","mic3","mic4","total"]
mic = ["total", "mic4", "mic3", "mic2", "mic1"]

# function that gets doa from the mic
def getDoa():
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
    if dev:
        Mic_tuning = Tuning(dev)
        print(Mic_tuning.direction)
    return(Mic_tuning.direction)

def getVad():
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
    if dev:
        Mic_tuning = Tuning(dev)
        print(Mic_tuning.is_voice())
    return(Mic_tuning.is_voice())



def getVolume(indata, outdata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10


y = np.arange(5)

def animate(i):
    # vol = getVolume()
    doa = getDoa()

    for i in range(len(volume)):
        volume[i] = doa

    if getVad():
        plt.barh(y, volume,  height = 0.4, color=("red"))
    else:
        plt.barh(y, volume,  height = 0.4)

    plt.yticks(y, mic)
plt.clf()
    
plt.title("Voice Activity Detection", fontdict = titleFont)
plt.xlim = ([0,360])
plt.ylim = ([0,360])



ani = FuncAnimation(plt.gcf(), animate, interval = 1000)

plt.show()
plt.clf()