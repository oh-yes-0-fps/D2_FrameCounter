from re import T
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

    start_bind = config["start_bind"]
    end_bind = config["end_bind"]
    weapon_ads_hold_bind = config["weapon_ads_hold_bind"]

sct = mss()


#         x,   y,   x,   y
# bounds = (163, 153, 182, 176)
# change from 1440p to screen size relative
bounds = (int(SCREEN_WIDTH_PX*0.0636), int(SCREEN_HEIGHT_PX*0.106),
          int(SCREEN_WIDTH_PX*0.075), int(SCREEN_HEIGHT_PX*0.118))

ads_times = []


def time_ads(repeat: int):
    ACTIVATED = False
    start_frame = np.array(sct.grab(bounds))
    start_time = 0
    for i in range(repeat):
        BREAK = False
        while True:
            if keyboard.is_pressed(end_bind):
                BREAK = True
                break
            if not ACTIVATED:
                keyboard.send(weapon_ads_hold_bind)  # hold zoom
                start_time = time.time()
                ACTIVATED = True
                continue
            if ACTIVATED:
                frame = np.array(sct.grab(bounds))
                diff_luminosity = abs(np.average(
                    frame) - np.average(start_frame))
                diff = np.average(cv2.absdiff(frame, start_frame))
                if diff_luminosity > 10 and diff > 8:
                    ads_times.append(time.time() - start_time)
                    # screen = np.array(sct.grab(sct.monitors[1]))
                    # cv2.imshow("screen", screen)
                    # cv2.waitKey(0)
                    keyboard.send(weapon_ads_hold_bind)  # release zoom
                    ACTIVATED = False
                    time.sleep(1.3)
                    break
        if BREAK:
            break


def average_time(times: list[float]):
    rough_avg = sum(times)/len(times)
    # remove value furthest from average
    times.remove(max(times, key=lambda x: abs(x - rough_avg)))
    return sum(times)/len(times)


print(f"Press {start_bind} to start timing ADS, {end_bind} to stop")
print(f"make sure alternate ads is bound to {weapon_ads_hold_bind}")
while True:
    if keyboard.is_pressed(end_bind):
        break
    if keyboard.is_pressed(start_bind):
        time_ads(4)
        print(f"Average ADS Time: {round(average_time(ads_times), 4)}s")
        ads_times = []
