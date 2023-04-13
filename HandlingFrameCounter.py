import keyboard
import cv2
from mss import mss
import numpy as np
import time

#delete all frames in the folder
import os
if not os.path.exists("frame_results"):
    os.mkdir("frame_results")
for filename in os.listdir("frame_results"):
    os.remove(f"frame_results\\{filename}")
SAVE_FRAMES = False


sct = mss()

# make a bounds tuple for just the center 10% of the screen for 1440p
bounds = (602*2, 335*2, 663*2, 392*2)


# always start on energy   weapon
kinetic_stows: list[float] = []
energy_stows: list[float] = []
kinetic_readies: list[float] = []
energy_readies: list[float] = []


change_id = [kinetic_stows, energy_readies, energy_stows, kinetic_readies]
change_id_str = ["kinetic_stows", "energy_readies", "energy_stows", "kinetic_readies"]

RELOAD_TIME = 1.9
BURST_TIME = 0


def time_weapons(repeat: int):
    should_switch_to_heavy = False
    switch_heavy = should_switch_to_heavy
    last_frame = np.array(sct.grab(bounds))
    ACTIVATED = False
    start_time = 0
    counter = 0
    for i in range(repeat*4):
        BREAK = False
        time_taken = 0
        while True:
            if keyboard.is_pressed(']'):
                keyboard.send('=')
                BREAK = True
                break
            if not ACTIVATED:
                if should_switch_to_heavy:
                    if switch_heavy:
                        keyboard.send('3')
                    else:
                        keyboard.send('2')
                    switch_heavy = not switch_heavy
                else:
                    keyboard.send(';')  # swap
                start_time = time.time()
                ACTIVATED = True
                time.sleep(0.1)
                keyboard.send('=', do_release=False)  # hold fire
                continue
            if ACTIVATED:
                frame = np.array(sct.grab(bounds))
                diff = np.average(cv2.absdiff(frame, last_frame))
                luminosity = np.average(frame)
                if diff > 2 and luminosity > 65.5 and luminosity < 89 and not i % 2:
                    time_taken = time.time() - start_time
                    change_id[i % 4].append(time_taken)
                    start_time = time.time()
                    # ACTIVATED = False
                    print(f"weapon swap {change_id_str[i % 4]}")
                    if SAVE_FRAMES:
                        cv2.imwrite(f"frame_results\\{change_id_str[i % 4]}_{counter}.png", frame)
                    # cv2.imshow("frame", frame)
                    # cv2.waitKey(0)
                    time.sleep(0.05)
                    counter += 1
                    # last_frame = np.array(sct.grab(bounds))
                    break
                if luminosity > 83 and diff > 5.5 and i % 2:
                    time_taken = time.time() - start_time
                    change_id[i % 4].append(time_taken)
                    start_time = time.time()
                    ACTIVATED = False
                    # keyboard.send('=')
                    keyboard.send('=', do_press=False)
                    print(f"Weapon shot {change_id_str[i % 4]}")
                    if SAVE_FRAMES:
                        cv2.imwrite(f"frame_results\\{change_id_str[i % 4]}_{counter}.png", frame)
                    time.sleep(BURST_TIME)
                    keyboard.send('r')
                    time.sleep(RELOAD_TIME)
                    counter += 1
                    last_frame = np.array(sct.grab(bounds))
                    break
                last_frame = frame
        if BREAK:
            break
    keyboard.send('=')


while True:
    if keyboard.is_pressed('['):
        break
    if keyboard.is_pressed(']'):
        time_weapons(3)
        break


def average_time(times: list[float]):
    rough_avg = sum(times)/len(times)
    #remove value furthest from average
    times.remove(max(times, key=lambda x: abs(x - rough_avg)))
    return sum(times)/len(times)


print(f"Kinetic Stow: {average_time(kinetic_stows)}s :: {kinetic_stows}")
print(f"Energy Stow: {average_time(energy_stows)}s :: {energy_stows}")
print(f"Kinetic Ready: {average_time(kinetic_readies)}s :: {kinetic_readies}")
print(f"Energy Ready: {average_time(energy_readies)}s :: {energy_readies}")