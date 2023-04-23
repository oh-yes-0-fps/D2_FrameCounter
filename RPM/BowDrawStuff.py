import keyboard
import cv2
from mss import mss
import numpy as np
import time

sct = mss()

buff_area_bounds = (60, 875, 115, 975)
# buff_area_bounds = (0, 0, 1440, 2560)
# buff_area_bounds = (820, 50, 950, 150)

ENDED = False
start_time = 0


def end(e):
    keyboard.send("=", do_press=False)
    global ENDED
    ENDED = True
keyboard.hook_key("[", end)

STARTED = False


def start(e):
    global start_time
    start_time = time.time()
    keyboard.send("=", do_release=False)
    global STARTED
    STARTED = True


keyboard.hook_key("]", start)

last_frame = np.array(sct.grab(buff_area_bounds))
while True:
    img = np.array(sct.grab(buff_area_bounds))
    if ENDED:
        break
    if not STARTED:
        last_frame = img
        continue
    if np.average(cv2.absdiff(img, last_frame)) > 0.15 and time.time() - start_time > 0.1:
        print(f"drawed: {time.time() - start_time}")
        last_frame = img
        STARTED = False
        keyboard.send("=", do_press=False)
