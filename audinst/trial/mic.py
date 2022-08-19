# Print out realtime audio volume as ascii bars
import time
import sounddevice as sd
import numpy as np
import copy
import socket
import pyaudio


MIC1 = False
MIC2 = False
MIC3 = False
MIC4 = False

def detected(device):
    print("detected func")
    if device == "MIC1":
        MIC1 = True
        print("mic1 is speaking")
    elif device == "MIC2":
        # MIC2 = True
        print("mic2 is speaking")
    elif device == "MIC3":
        # MIC3 = True
        print("mic3 is speaking")
    elif device == "MIC4":
        # MIC4 = True
        print("mic4 is speaking")


def report():
    return (MIC1, MIC2, MIC3, MIC4)