# %%
import threading
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import math
import time
import sys
import pyglet

NUM_LED = 64
root = int(math.sqrt(NUM_LED))

# %%
# Store as string representation of colour of hex ie '#0f0f0f'
DEFAULT_COLOUR = '#ffffff'      # White
arr_led = [DEFAULT_COLOUR for i in range(NUM_LED)]

x_val = []
for i in range(root):
    x_val = np.append(x_val, np.arange(start=1, stop=root+1))

y_val = []
for i in range(root):
    y_val = np.append(y_val, (i+1)*np.ones(root, dtype=int))

# %%
# Amplitude/brightness function
SCALE = 8

def get_size(led_colour: str) -> int:
    led_colour = led_colour.split('#')[1]
    BIT_CHK = 0xFF
    BYTE = 8
    size = int(led_colour, base=16)
    max = 0
    while size > 0:
        temp = size & BIT_CHK
        if temp > max:
            max = temp
        size = size >> BYTE
    return max
# %%
def led_scatter(colours: list):
    led_size = [SCALE*get_size(led) for led in colours]
    plt.clf()
    plt.scatter(x_val, y_val, s=led_size, c=colours, alpha=0.70, edgecolors='grey')
    plt.xlim([-1, 10])
    plt.ylim([0, 9])
# %%
def random_colour() -> str:
    colour = str(hex(np.random.randint(0, 0xffffff))).replace('0x', '#')
    while len(colour) < 7:
        colour = colour.replace('#', '0')
        colour = '#'+colour
    return colour

def generate_random() -> list:
    led_arr = [random_colour() for led in range(NUM_LED)]
    return led_arr

# %%
FPS = 30
INTERVAL = 1/FPS
# %%

sound = AudioSegment.from_mp3('data/lofi-type-beat.mp3')
music_thread = threading.Thread(target=play, args=(sound,))

def rgb2hex(r,g,b):
    r = int(255*r)
    g = int(255*g)
    b = int(255*b)
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

frames = np.load('./values/frames.npy')

def animate(i):
    global music_start, music_thread
    if i == 0:
        if not music_thread.is_alive():
            music_thread.start()
            music_start = time.perf_counter()
    prev_i=i
    j = (time.perf_counter() - music_start)*FPS
    i = int(j)
    # ratio = j - i
    # print(prev_i, i)
    frame = frames[i]
    flattened = frame.reshape(-1, 3)
    as_hex = [rgb2hex(*rgb) for rgb in flattened]
    led_scatter(as_hex)

ani = FuncAnimation(plt.gcf(), animate, interval=INTERVAL)

plt.show()


# %%
