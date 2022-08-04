# volume.py
# Print out realtime audio volume as ascii bars

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

init = True

while True:

    present_wave = []
    compare_wave = []

    # print volume 
    def print_sound(indata, outdata, frames, time, status):
        # volume calculation
        volume_norm = np.linalg.norm(indata)*10
        # priting volume
        print("|" * int(volume_norm))

        # append the current wave to to array 
        present_wave.append(gijunjum - volume_norm)

    # use Stream to print
    with sd.Stream(callback=print_sound, latency = 0.5):
        sd.sleep(duration * 1000)

    if init is True:
        prev_wave = copy.copy(present_wave)
        init = False

    try:
        for idx, each in enumerate(present_wave):
            compare_wave.append(each - prev_wave[idx])
    except IndexError:
        pass

    temp = 0
    total_change = 0
    for cw in compare_wave:
        if abs(cw - temp) > 4:
            total_change = total_change + 1

        temp = cw

    if total_change > 30:
        print("sound detect!!")
        client_socket.sendto(data, cli)

    time.sleep(0.01)