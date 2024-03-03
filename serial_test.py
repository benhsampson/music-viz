import serial
import time
import numpy as np

arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.1)

frames = 100*np.ones(192, dtype=np.byte)
frames = frames.tobytes() + b'\r'

frames2 = np.zeros(192, dtype=np.byte)
frames2 = frames2.tobytes() +b'\r'

def write_read(x):
    arduino.write(x)
    return 

while True:
    write_read(frames)
    time.sleep(1/50)
    write_read(frames2)

    