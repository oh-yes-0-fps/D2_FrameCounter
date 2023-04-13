from re import T
import keyboard
import cv2
from mss import mss
import numpy as np
import time



sct = mss()

# make a bounds tuple for just the center 10% of the screen for 1440p
bounds = (163, 153, 182, 176)

ads_times = []

def time_ads(repeat: int):
    ACTIVATED = False
    start_frame = np.array(sct.grab(bounds))
    start_time = 0
    for i in range(repeat):
        BREAK = False
        while True:
            if keyboard.is_pressed(']'):
                BREAK = True
                break
            if not ACTIVATED:
                keyboard.send('-')  # hold zoom
                start_time = time.time()
                ACTIVATED = True
                continue
            if ACTIVATED:
                frame = np.array(sct.grab(bounds))
                diff_luminosity = abs(np.average(frame) - np.average(start_frame))
                diff = np.average(cv2.absdiff(frame, start_frame))
                if diff_luminosity > 10 and diff > 8:
                    ads_times.append(time.time() - start_time)
                    # screen = np.array(sct.grab(sct.monitors[1]))
                    # cv2.imshow("screen", screen)
                    keyboard.send('j')  # release zoom
                    ACTIVATED = False
                    #get entire screen
                    cv2.waitKey(0)
                    time.sleep(1.3)
                    break
        if BREAK:
            break


def average_time(times: list[float]):
    rough_avg = sum(times)/len(times)
    #remove value furthest from average
    times.remove(max(times, key=lambda x: abs(x - rough_avg)))
    return sum(times)/len(times)


print("Press [ to start timing ADS, ] to stop")
print("make sure alternate ads is bound to minus(-)")
while True:
    if keyboard.is_pressed(']'):
        break
    if keyboard.is_pressed('['):
        time_ads(4)
        print(f"Average ADS Time: {round(average_time(ads_times), 4)}s")
        ads_times = []