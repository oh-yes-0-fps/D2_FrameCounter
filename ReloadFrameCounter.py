import keyboard
import cv2
from mss import mss
import numpy as np
import time


with open("config.json", "r") as f:
    import json
    config = json.load(f)
    ALPHA_THRSHOLD = config["alphaThreshold"]
    SCREEN_WIDTH_PX = config["screenWidth"]
    SCREEN_HEIGHT_PX = config["screenHeight"]

    fire_bind = config["fire_bind"]
    start_bind = config["start_bind"]
    end_bind = config["end_bind"]
    reload_bind = config["reload_bind"]


sct = mss()

PERCENT_FROM_CENTER_OF_SCREEN = 0.05

scl = PERCENT_FROM_CENTER_OF_SCREEN/2.0
crosshair_bounds = (int(SCREEN_WIDTH_PX*(0.5-scl)), int(SCREEN_HEIGHT_PX*(0.5-scl)), int(SCREEN_WIDTH_PX*(0.5+scl)), int(SCREEN_HEIGHT_PX*(0.5+scl)))
ammo_bounds = (int(SCREEN_WIDTH_PX*0.215), int(SCREEN_HEIGHT_PX*0.85), int(SCREEN_WIDTH_PX*0.27), int(SCREEN_HEIGHT_PX*0.88))

ACTIVATED = False
has_ammo_counter = False
needs_ammo_counter = False
ammo_counter = np.array(sct.grab(ammo_bounds))
start_time = 0
time_taken = 0

ammo_time = 0

print(f"Press {start_bind} to start, {end_bind} to stop\n",
      f"Have alternate shoot bound to {fire_bind}")
while True:
    if keyboard.is_pressed(end_bind):
        keyboard.send(fire_bind, do_press=False)
        break
    if keyboard.is_pressed(start_bind):
        keyboard.send(fire_bind)#fire
        keyboard.send(reload_bind)#reload
        start_time = time.time()
        ACTIVATED = True
        has_ammo_counter = False
        needs_ammo_counter = True
        ammo_time = 0
        keyboard.send(fire_bind, do_release=False)#hold fire
        time.sleep(0.66)#bullet hole luminance stays for a bit
        continue
    if ACTIVATED:
        frame = np.array(sct.grab(crosshair_bounds))
        # cv2.imshow("frame", frame)
        # cv2.waitKey(120)
        if time.time() - start_time > 0.1 and not has_ammo_counter:
            ammo_counter = np.array(sct.grab(ammo_bounds))
            has_ammo_counter = True
        if has_ammo_counter and needs_ammo_counter:
            #get difference between frames
            curr_ammo_counter = np.array(sct.grab(ammo_bounds))
            diff = np.average(cv2.absdiff(curr_ammo_counter, ammo_counter))
            if diff > 1.0:
                ammo_time_taken = time.time() - start_time
                ammo_time = ammo_time_taken
                print(f"Ammo Time: {ammo_time_taken}s")
                has_ammo_counter = False
                needs_ammo_counter = False
        #get avg luminosity of frame
        avg_luminosity = np.average(frame)
        if avg_luminosity > ALPHA_THRSHOLD:
            time_taken = time.time() - start_time
            keyboard.send(fire_bind, do_press=False)
            print(f"Reload Time: {round(time_taken-(1/100),4)}s")
            print(f"Percent for ammo {(ammo_time/(time_taken-(1/100)))*100}%")
            ACTIVATED = False
            time.sleep(0.2)
keyboard.send(fire_bind, do_press=False)

