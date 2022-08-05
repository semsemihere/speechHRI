# speech.py
# speech recognition sample file

import speech_recognition as sr

# mic = 'USB PnP Audio Device: Audio (hw:2,0)'
mic = 'USB Audio Device: - (hw:2,0)'


sample_rate = 48000

chunk_size = 2048

r = sr.Recognizer()

mic_list = sr.Microphone.list_microphone_names()

for i, microphone_name in enumerate(mic_list):
    if microphone_name == mic:
        deviceId = i

m1 = sr.Microphone(device_index = deviceId, sample_rate = sample_rate, chunk_size = chunk_size)

with m1 as source:
    r.adjust_for_ambient_noise(source)
    print("Say something")
    audio = r.listen(source)
    print(audio)

    try:
        print(r.recognize_google(audio))

        text = r.recognize_google(audio)
        print("you said: " + text)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")

    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}")

