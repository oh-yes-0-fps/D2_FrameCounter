import os
import keyboard
from mss import mss
import numpy as np

with open("config.json", "r") as f:
    import json
    config = json.load(f)
    SCREEN_WIDTH_PX = config["screenWidth"]
    SCREEN_HEIGHT_PX = config["screenHeight"]

    start_bind = config["start_bind"]
    end_bind = config["end_bind"]

ASPECT_RATIO = SCREEN_WIDTH_PX/SCREEN_HEIGHT_PX
PERCENT_FROM_CENTER_OF_SCREEN = 0.1


x_scl = PERCENT_FROM_CENTER_OF_SCREEN/2.0
y_scl = min((PERCENT_FROM_CENTER_OF_SCREEN/2.0)*ASPECT_RATIO, SCREEN_HEIGHT_PX)
crosshair_bounds = (int(SCREEN_WIDTH_PX*(0.5-x_scl)), int(SCREEN_HEIGHT_PX*(0.5-y_scl)),
                    int(SCREEN_WIDTH_PX*(0.5+x_scl)), int(SCREEN_HEIGHT_PX*(0.5+y_scl)))

sct = mss()

while True:
    matrix = np.array(sct.grab(crosshair_bounds))
    tl = matrix[0, 0]
    tr = matrix[0, matrix.shape[1]-1]
    bl = matrix[matrix.shape[0]-1, 0]
    br = matrix[matrix.shape[0]-1, matrix.shape[1]-1]
    bg_avg = np.average([tl, tr, bl, br], axis=0)
    print(f"R: {bg_avg[2]}, G: {bg_avg[1]}, B: {bg_avg[0]}")