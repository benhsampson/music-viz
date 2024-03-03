import serial
import time 
import numpy as np

arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1) 

FPS = 30
INTERVAL = 1/30

frames = np.load('values/sunflower.npy')

i = 0
while True: 
    print(frames[i])
    
    full = 100*np.ones(192, dtype = np.byte)
    array = full.tobytes() + b'\n'
    print(array)
    arduino.write(array)

    time.sleep(2)

    x = arduino.readline()
    print(x)
    
    i += 1
    
    if i > 0:
        break

    time.sleep(INTERVAL)
