import keyboard
# import cv2
from mss import mss
import numpy as np
# import time

with open("config.json", "r") as f:
    import json
    config = json.load(f)
    SCREEN_WIDTH_PX = config["screenWidth"]
    SCREEN_HEIGHT_PX = config["screenHeight"]

    start_bind = config["start_bind"]
    end_bind = config["end_bind"]

HORIZONTAL = False  # if false will use vertical

# pixle offset from the middle most pixel of the axis
PIXEL_OFFSET = 0

DESIRED_COLOR = "G"


PERCENT_FROM_CENTER_OF_SCREEN = 0.05

scl = PERCENT_FROM_CENTER_OF_SCREEN/2.0
crosshair_bounds = (int(SCREEN_WIDTH_PX*(0.5-scl)), int(SCREEN_HEIGHT_PX*(0.5-scl)),
                    int(SCREEN_WIDTH_PX*(0.5+scl)), int(SCREEN_HEIGHT_PX*(0.5+scl)))

sct = mss()


def get_verticle_in_matrix(matrix: np.ndarray, pixel_offset: int):
    return matrix[:, matrix.shape[1]//2 + pixel_offset]


def get_horizontal_in_matrix(matrix: np.ndarray, pixel_offset: int):
    return matrix[matrix.shape[0]//2 + pixel_offset, :]

def get_color_from_pixel_array(pixel_matrix: np.ndarray, color_idx: int):
    return pixel_matrix[:, color_idx]

def get_first_half_of_matrix(array: np.ndarray):
    return array[:array.shape[0]//2]

def rgb_idx():
    if DESIRED_COLOR == "R":
        return 0
    elif DESIRED_COLOR == "G":
        return 1
    elif DESIRED_COLOR == "B":
        return 2
    else:
        raise Exception("Invalid desired color")

def get_normalized_reticle_shading(matrix: np.ndarray):
    # get the 4 corners of the matrix and average the colors
    tl = matrix[0, 0]
    tr = matrix[0, matrix.shape[1]-1]
    bl = matrix[matrix.shape[0]-1, 0]
    br = matrix[matrix.shape[0]-1, matrix.shape[1]-1]
    background_color = np.average([tl, tr, bl, br], axis=0)[rgb_idx()]

    if HORIZONTAL:
        _1d_matrix = get_horizontal_in_matrix(matrix, PIXEL_OFFSET)
    else:
        _1d_matrix = get_verticle_in_matrix(matrix, PIXEL_OFFSET)
    pixel_map = get_first_half_of_matrix(_1d_matrix)
    color_map = list(get_color_from_pixel_array(pixel_map, rgb_idx()))
    color_map = [min(x-background_color, 0.0) for x in color_map]
    max_val = max(color_map)
    if max_val == 0:
        return color_map
    color_map = [x/max_val for x in color_map]
    return list(color_map)


def get_screenshot() -> np.ndarray:
    return np.array(sct.grab(crosshair_bounds))


print(f"Press {start_bind} to start, {end_bind} to stop")


run_is_down = False
def run(args: keyboard.KeyboardEvent):
    global run_is_down
    if not run_is_down:
        print(get_normalized_reticle_shading(get_screenshot()))
    if args.event_type == "down":
        run_is_down = True
    if args.event_type == "up":
        run_is_down = False


exit_val = False
def stop(*args):
    print("Exiting")
    keyboard.unhook_all()
    global exit_val
    exit_val = True


keyboard.hook_key(key=start_bind, callback=run, suppress=True)
keyboard.hook_key(key=end_bind, callback=stop)

while True:
    if exit_val:
        exit()
