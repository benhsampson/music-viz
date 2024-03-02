# %%
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import math
import time
import sys

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
FRAMES = 30
# %%
def animate(i):
    led_arr = generate_random()
    led_scatter(led_arr)

ani = FuncAnimation(plt.gcf(), animate, interval=INTERVAL)

plt.show()
