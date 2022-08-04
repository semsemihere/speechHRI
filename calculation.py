# calculation.py
# calculating manually using equations

from cmath import acos
import speech_recognition as sr
import time
import math
import asyncio

# mic1 = 'USB PnP Audio Device: Audio (hw:2,0)'
mic1 = 'USB Audio Device: - (hw:2,0)'
mic2 = "USB Audio Device: - (hw:3,0)"
mic3 = "USB Audio Device: - (hw:4,0)"
mic4 = "USB Audio Device: - (hw:5,0)"

# current temperature
temp = 26
# speed of sound
vs = 330 + (0.6 * temp) 

# distance btw microphones; cm
d = 10

sample_rate = 48000

chunk_size = 2048

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



# t1 = getMic(deviceId1)

# t2 = getMic(deviceId2)

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(getMic(deviceId1), getMic(deviceId2)))


# timeInterval = t2 - t1 
# print('t1: ', t1, ' t2: ', t2, ' tI: ', timeInterval)


# theta = math.acos(((vs * timeInterval) / d ))


# print(theta)
