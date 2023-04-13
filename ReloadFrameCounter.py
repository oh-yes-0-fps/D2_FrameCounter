import keyboard
import cv2
from mss import mss
import numpy as np
import time

#CONFIG VARIABLES
ALPHA_THRSHOLD = 100
SCREEN_WIDTH_PX = 2560
SCREEN_HEIGHT_PX = 1440


sct = mss()

crosshair_bounds = (int(SCREEN_WIDTH_PX*0.475), int(SCREEN_HEIGHT_PX*0.475), int(SCREEN_WIDTH_PX*0.525), int(SCREEN_HEIGHT_PX*0.525))
ammo_bounds = (int(SCREEN_WIDTH_PX*0.215), int(SCREEN_HEIGHT_PX*0.85), int(SCREEN_WIDTH_PX*0.27), int(SCREEN_HEIGHT_PX*0.88))

ACTIVATED = False
has_ammo_counter = False
needs_ammo_counter = False
ammo_counter = np.array(sct.grab(ammo_bounds))
start_time = 0
time_taken = 0

ammo_time = 0

print("Press [ to start, ] to stop\n",
      "Have alternate shoot bound to equals(=)")
while True:
    if keyboard.is_pressed(']'):
        keyboard.send('=', do_press=False)
        break
    if keyboard.is_pressed('['):
        keyboard.send('=')#fire
        keyboard.send('r')#reload
        start_time = time.time()
        ACTIVATED = True
        has_ammo_counter = False
        needs_ammo_counter = True
        ammo_time = 0
        keyboard.send('=', do_release=False)#hold fire
        time.sleep(0.66)#bullet hole luminance stays for a bit
        continue
    if ACTIVATED:
        frame = np.array(sct.grab(crosshair_bounds))
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
            keyboard.send('=', do_press=False)
            print(f"Reload Time: {round(time_taken-(1/100),4)}s")
            print(f"Percent for ammo {(ammo_time/(time_taken-(1/100)))*100}%")
            ACTIVATED = False
            time.sleep(0.2)

