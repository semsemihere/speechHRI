# calculation.py
# calculating manually using equations
import wave
import sounddevice as sd
import numpy as np
import copy
import socket
import time
import pyaudio
import wave
import sys
import matplotlib.pyplot as plt
from scipy.io import wavfile
# %matplotlib inline
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import count



# mic1 = 'USB PnP Audio Device: Audio (hw:2,0)'
mic1 = 'USB Audio Device: - (hw:2,0)'
mic2 = "USB Audio Device: - (hw:3,0)"
mic3 = "USB Audio Device: - (hw:4,0)"
mic4 = "USB Audio Device: - (hw:5,0)"

#### Fixed values
# current temperature
temp = 26
# speed of sound
vs = 330 + (0.6 * temp) 

sample_rate = 48000

#### Flexible values
# initialized values
D = 10 # init distance; cm
S = 300 #init sound intensity; dB

# distance btw microphones; cm
# d = 10




audio = pyaudio.PyAudio()

for idx in range(audio.get_device_count()):
    desc = audio.get_device_info_by_index(idx)
    print("Device:{}, INDEX:{}, RATE:{}".format(desc["name"], idx, int(desc["defaultSampleRate"])))

 
CHUNK = 2*10 # brings chunk amount of data at once
FORMAT = pyaudio.paInt16 # sets the depht of the bit; Int16 == depth is 16 bit
CHANNELS = 1
RATE = 44100 # sampling rate 
DEVICE_INDEX = 24 # sets the location of the mic
 
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
              frames_per_buffer=CHUNK, input_device_index=DEVICE_INDEX)

D1 = 50
# indata = np.fromstring(stream.read(512),dtype=np.int16)
S1 = 200
# print(D1, S1)
    

for i in range(0, int(RATE / CHUNK * 10)):
    # get sound data and print
    data = np.fromstring(stream.read(CHUNK),dtype=np.int16) 
        # stream.read(CHUNK); converts sound data to string
        # np.fromstring(dtype=np.int16); converts the string to 16bit numpy array
    

    volume = int(np.average(np.abs(data)))

    # dist = D1 // (10**((volume - S1) / 20))
    dist = 0
    print("vol:", volume, " dist: ", dist)
    # time.sleep(1)


stream.stop_stream()
stream.close()
p.terminate()


""" 
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

SPEED_OF_SOUND = 34300 # cm/s
DENSITY_OF_MEDIUM = 0.001225 # g/cm3 

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)



#recording
print("Start to record the audio.")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording is finished.")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()



######## Calculation

# plt.rcParams['figure.dpi'] = 100
# plt.rcParams['figure.figsize'] = (9, 7)

# sampFreq, sound = wavfile.read("data_noise_a3s.wav")

# print(sound.dtype, sampFreq) # int16 (16 bit)
# sound = sound / 2.0**15
# print(sound)

# print(sound.shape)
# length_in_s = sound.shape[0] / sampFreq
# print(length_in_s)

print("------------------")
sampFreq, sound = wavfile.read("data_noise_a3s.wav")

# sampFreq, sound = wavfile.read("output.wav")
print(sound.dtype, sampFreq) # int16 (16 bit)
sound = sound / 2.0**15
print(sound.shape) # returns (sample points, channel count)
length_in_s = sound.shape[0] / sampFreq
print(length_in_s)

signal = sound[:,0]

# Fourier transform 
# fft.rfft: computes the one-dimensional discrete Fourier transform for real input
fft_spectrum = np.fft.rfft(signal)  
freq = np.fft.rfftfreq(signal.size, d=1./sampFreq)
fft_spectrum_abs = np.abs(fft_spectrum)
print(fft_spectrum_abs)

for i,f in enumerate(fft_spectrum_abs):
    if f > 350: #looking at amplitudes of the spikes higher than 350 
        print("here:", i, f)
        frequency = np.round(freq[i],1) // 10
        amplitude = np.round(f) // 10
        
        soundIntensity = 2 * (math.pi**2) * (frequency **2) * (amplitude ** 2) * 413.3
        # volume_norm = np.linalg.norm(indata)*10
        print('frequency = {} Hz with amplitude {} and Sound Intensity is {}'.format(frequency, amplitude, soundIntensity))




# plt.plot(freq[:3000], np.abs(fft_spectrum[:3000]))
# plt.xlabel("frequency, Hz")
# plt.ylabel("Amplitude, units")
# plt.show()

"""



"""
# playing
if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

data = wf.readframes(CHUNK)

while data != '':
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()
"""










###### Speech Recognition
"""

r = sr.Recognizer()

mic_list = sr.Microphone.list_microphone_names()

# print(mic_list)

for i, microphone_name in enumerate(mic_list):
    if microphone_name == mic1:
        deviceId1 = i
    elif microphone_name == mic2:
        deviceId2 = i

async def getMic(devinceId):
    s = sr.Microphone(device_index = deviceId1, sample_rate = sample_rate, chunk_size = chunk_size)

    with s as source:
        r.adjust_for_ambient_noise(s)
        print("Say something")

        audio1 = r.listen(s)
        
    
        if (r.recognize_google(audio1)):
            t = time.time()
            # text = r.recognize_google(audio1)
            # print("you said: " + text)
            
    print(t)

"""
