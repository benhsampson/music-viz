import serial
import time 
import numpy as np

arduino = serial.Serial(port='COM4', baudrate=9600, timeout=.1) 

FPS = 30
INTERVAL = 1/30

frames = np.load('values/sunflower.npy')

i = 0
while True:
    # print(frames[i].shape)
    # array = bytearray(frames[i])
    # full = 100*np.ones((192)).astype(int)

    # print(full)
    # array = bytearray(full) + b'\n'
    # print(array)
    # arduino.write(array)
    
    # array = b''
    # for i in range(192):
    #     array += bytes(100)
    # array += b'\n'
    # print(array)
    
    print(frames[i])
    
    full = 100*np.ones(192, dtype = np.byte)
    array = full.tobytes() + b'\n'
    print(array)
    arduino.write(array)

    x = arduino.read(192)
    print(x)
    
    i += 1
    
    if i > 0:
        break

    time.sleep(INTERVAL)
