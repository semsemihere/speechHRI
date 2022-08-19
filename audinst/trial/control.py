import mic
import subprocess
import time
import os


os.system('python mic1.py')

while True:
    status = mic.report()
    time.sleep(0.1)


    print(status)