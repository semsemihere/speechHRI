# Print out realtime audio volume as ascii bars
import time
import sounddevice as sd
import numpy as np
import copy
import mic

error_wave = ''

gijunjum = 1000

duration = 3  # seconds

prev_wave = []

init = True

# print(sd.query_devices())

sd.default.device = 27

while True:

    present_wave = []
    compare_wave = []

    def print_sound(indata, outdata, frames, time, status):
        volume_norm = np.linalg.norm(indata)*10
        print("mic4: ", "|" * int(volume_norm))

        present_wave.append(gijunjum - volume_norm)

    with sd.Stream(callback=print_sound):
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

    if total_change > 10:
        print("mic4 sound detect!!")
        mic.detected("MIC4")

    time.sleep(0.01)
