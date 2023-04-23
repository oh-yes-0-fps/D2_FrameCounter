from enum import Enum
import os
import keyboard
from mss import mss
import numpy as np
import cv2
# import time


FILE_NAME = "./Cones/aa_frame_data_scout_fps.json"
RENDER_RESOLUTION = 200


with open("config.json", "r") as f:
    import json
    config = json.load(f)
    SCREEN_WIDTH_PX = config["screenWidth"]
    SCREEN_HEIGHT_PX = config["screenHeight"]

    start_bind = config["start_bind"]
    end_bind = config["end_bind"]

class Direction(Enum):
    HORIZONTAL = 0
    VERTICAL = 1
    DIAGONAL = 2

# pixle offset from the middle most pixel of the axis
PIXEL_OFFSET = 0

DESIRED_COLOR = "G"


ASPECT_RATIO = SCREEN_WIDTH_PX/SCREEN_HEIGHT_PX
PERCENT_FROM_CENTER_OF_SCREEN = 0.1


x_scl = PERCENT_FROM_CENTER_OF_SCREEN/2.0
y_scl = min((PERCENT_FROM_CENTER_OF_SCREEN/2.0)*ASPECT_RATIO, SCREEN_HEIGHT_PX)
crosshair_bounds = (int(SCREEN_WIDTH_PX*(0.5-x_scl)), int(SCREEN_HEIGHT_PX*(0.5-y_scl)),
                    int(SCREEN_WIDTH_PX*(0.5+x_scl)), int(SCREEN_HEIGHT_PX*(0.5+y_scl)))

sct = mss()


def get_verticle_in_matrix(matrix: np.ndarray, pixel_offset: int):
    return matrix[:, matrix.shape[1]//2 + pixel_offset]


def get_horizontal_in_matrix(matrix: np.ndarray, pixel_offset: int):
    return matrix[matrix.shape[0]//2 + pixel_offset, :]

def get_diagonal_in_matrix(matrix: np.ndarray, pixel_offset: int):
    new_matrix = []
    for i in range(matrix.shape[0]):
        try:
            new_matrix.append(matrix[matrix.shape[0]-i-1, i + pixel_offset])
        except IndexError:
            pass
    new_matrix = np.array(new_matrix)
    len_diff = matrix.shape[0] - new_matrix.shape[0]
    #cutoff half of len diff from each side
    new_matrix = new_matrix[len_diff//2:matrix.shape[0] - len_diff//2]
    return new_matrix

def get_color_from_pixel_array(pixel_matrix: np.ndarray, color_idx: int):
    return pixel_matrix[:, color_idx]


def get_first_half_of_matrix(array: np.ndarray):
    return array[:array.shape[0]//2]


def rgb_idx():
    if DESIRED_COLOR == "R":
        return 2
    elif DESIRED_COLOR == "G":
        return 1
    elif DESIRED_COLOR == "B":
        return 0
    else:
        raise Exception("Invalid desired color")


def get_normalized_reticle_shading(matrix: np.ndarray, direction: Direction, offset: int):

    # get the 4 corners of the matrix and average the colors
    tl = matrix[0, 0]
    tr = matrix[0, matrix.shape[1]-1]
    bl = matrix[matrix.shape[0]-1, 0]
    br = matrix[matrix.shape[0]-1, matrix.shape[1]-1]
    bg_avg = np.average([tl, tr, bl, br], axis=0)
    background_color = bg_avg[rgb_idx()]

    if background_color > 0:
        raise Exception("Background is too bright")

    if direction == Direction.HORIZONTAL:
        _1d_matrix = get_horizontal_in_matrix(matrix, offset)
    elif direction == Direction.VERTICAL:
        _1d_matrix = get_verticle_in_matrix(matrix, offset)
    else:
        _1d_matrix = get_diagonal_in_matrix(matrix, offset)
    pixel_map = get_first_half_of_matrix(_1d_matrix)
    color_map = list(get_color_from_pixel_array(pixel_map, rgb_idx()))
    #get highest value in color map
    max_val_output = int(max(color_map))
    color_map = [max(x-background_color, 0.0) for x in color_map]
    max_val = max(color_map)
    if max_val == 0:
        raise Exception(f"No color found {direction}")
    full_screen_range = SCREEN_WIDTH_PX/2
    color_map = [(x/max_val, (len(color_map) - i)/full_screen_range)
                 for i, x in enumerate(color_map)]
    return (list(color_map), max_val_output)

def get_screenshot() -> np.ndarray:
    return np.array(sct.grab(crosshair_bounds)) # type: ignore


if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w") as f:
        json.dump({}, f)
while True:
    inp = input("enter aim assist: ")
    adjuster_mod = False
    targeting_mods = 0
    if inp == "exit":
        exit()
    if "del" in inp:
        with open(FILE_NAME, "r") as f:
            jdata: dict[str, dict] = json.load(f)
        aa = inp.removeprefix("del ")
        del jdata[aa]
        with open(FILE_NAME, "w") as f:
            json.dump(jdata, f)
        continue
    if "a" in inp:
        adjuster_mod = True
        inp = inp.replace("a", "")
    if "t" in inp:
        split_inp = inp.split("t")
        aa = int(split_inp[0])
        targeting_mods = int(split_inp[1])
    elif inp == "ls":
        with open(FILE_NAME, "r") as f:
            jdata: dict[str, dict] = json.load(f)
        lst = list(jdata.keys())
        lst.sort()
        for a in lst:
            output = f"{a}: "
            output += f"mods: {jdata[a].get('targeting_mods_tested', [])}"
            output += f", adjuster: {jdata[a].get('adjuster_mod', False)}"
            print(output)
        print(f"total: {len(lst)}")
        continue
    else:
        aa = int(inp)
    screenshot = get_screenshot()
    cv2.imwrite("test.png", screenshot)
    result_h = get_normalized_reticle_shading(screenshot, Direction.HORIZONTAL, PIXEL_OFFSET)
    result_v = get_normalized_reticle_shading(screenshot, Direction.VERTICAL, PIXEL_OFFSET)
    result_d = get_normalized_reticle_shading(screenshot, Direction.DIAGONAL, PIXEL_OFFSET)

    with open(FILE_NAME, "r") as f:
        jdata: dict[str, dict] = json.load(f)
    t_mods = set(jdata.get(f"{aa}", {}).get("targeting_mods_tested", []))
    t_mods.add(targeting_mods)
    info = {
        "screen_height": SCREEN_HEIGHT_PX,
        "screen_width": SCREEN_WIDTH_PX,
        "render_resolution": RENDER_RESOLUTION,
        "color": DESIRED_COLOR,
        "targeting_mods_tested": list(t_mods),
        "adjuster_mod": adjuster_mod,
        "data_t0": jdata.get(f"{aa}", {}).get("data_t0", {}),
        "data_t1": jdata.get(f"{aa}", {}).get("data_t1", {}),
        "data_t2": jdata.get(f"{aa}", {}).get("data_t2", {}),
        "data_t3": jdata.get(f"{aa}", {}).get("data_t3", {}),
    }
    if jdata.get(f"{aa}", {}).get(f"data_t{targeting_mods}", {}) != {}:
        confirm = input("WARNING: overwriting existing data, continue? (y/n) ")
        if confirm != "y":
            continue
    with open(FILE_NAME, "r") as f:
        jdata: dict[str, dict] = json.load(f)
    info[f"data_t{targeting_mods}"] = {
        "horizontal": result_h[0], "vertical": result_v[0], "diagonal": result_d[0],
        "horizontal_peak": result_h[1], "vertical_peak": result_v[1], "diagonal_peak": result_d[1],}
    jdata[f"{aa}"] = info
    with open(FILE_NAME, "w") as f:
        json.dump(jdata, f)
