import cv2
import numpy as np
import json

BURST_SIZE = 1

with open("config.json", "r") as f:
    config = json.load(f)
HEIGHT_OFFSET = config["heightOffset"]
WIDTH_OFFSET = config["widthOffset"]

with open("resources\\numbers.json", "r") as f:
    NUMBERS = json.load(f)

#delete all frames in the folder
import os
for filename in os.listdir("frame_results"):
    os.remove(f"frame_results\\{filename}")

def is_white_rgb(color_array:np.ndarray):
    r = int(color_array[0])
    g = int(color_array[1])
    b = int(color_array[2])
    needed_alpha = 130
    if r > needed_alpha and g > needed_alpha and b > needed_alpha:
        if abs(r - g) < 20 and abs(r - b) < 20 and abs(g - b) < 20:
            return True
    return False

def is_white_gray(a: int):
    a = int(a)
    needed_alpha = 135
    if a > needed_alpha:
            return True
    return False


out_jdata = {}

def frameToNumber(frame:np.ndarray, rgb:bool=False):
    num_data = {}
    is_white = is_white_rgb if rgb else is_white_gray
    for num in NUMBERS:
        matches = 0
        num_def = NUMBERS[num]
        total_matches = len(num_def["true"]) + len(num_def["false"])
        for coord in num_def["true"]:
            if is_white(frame[coord[1]+HEIGHT_OFFSET][coord[0]+WIDTH_OFFSET]):
                matches += 1
        for coord in num_def["false"]:
            if not is_white(frame[coord[1]+HEIGHT_OFFSET][coord[0]+WIDTH_OFFSET]):
                matches += 1
        num_data[num] = matches / total_matches
    out_jdata[frame_num] = num_data
    return max(num_data, key=num_data.get)


def analyze_video(file_path:str):
    cap = cv2.VideoCapture(file_path)

    fps = cap.get(cv2.CAP_PROP_FPS)

    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    if width/height != 16/9:
        raise Exception("Aspect ratio is not 16:9")

    shoot_frame_list = []
    shot_delay_list = []
    last_frame:int = 10
    while cap.isOpened():
        # get the current frame
        ret, frame = cap.read()

        # check if the frame is empty
        if not ret:
            break

        #resive frame to 720p
        frame = cv2.resize(frame, (1280, 720))

        # get the current frame number
        global frame_num
        frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)

        # look for a change in the number at 385x 600y
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #increase contrast
        frame_gray = cv2.addWeighted(frame_gray, 1.5, np.zeros(frame_gray.shape, frame_gray.dtype), 0, 0)

        #increase black level (darken)
        frame_gray = cv2.add(frame_gray, np.array([-80.0]))

        if HEIGHT_OFFSET == 0 or WIDTH_OFFSET == 0:
            cv2.imwrite(f"frame_results\\reference.png", frame_gray)
            print("setup pixel offssets in config.json")
            exit(0)
        num = frameToNumber(frame_gray)
        if frame_num > 1 and num != last_frame:
            if shoot_frame_list:
                shot_delay_list.append((frame_num - shoot_frame_list[-1])/30)
            shoot_frame_list.append(frame_num)
            cv2.imwrite(f"frame_results\\frame_{int(frame_num)}_is_{num}.png", frame_gray)
        last_frame = num

    is_burst = BURST_SIZE > 1
    if is_burst:
        burst_delay_num = []
        inter_burst_delay_num = []
        for i in range(len(shot_delay_list)):
            if i % BURST_SIZE:
                inter_burst_delay_num.append(shot_delay_list[i])
            else:
                burst_delay_num.append(shot_delay_list[i])
        print(f"burst_delay: {sum(burst_delay_num) / len(burst_delay_num)}")
        print(f"inter_burst_delay: {sum(inter_burst_delay_num) / len(inter_burst_delay_num)}")
        print(f"burst duration: {(sum(inter_burst_delay_num) / len(inter_burst_delay_num))*(BURST_SIZE-1)}")
    else:
        print(f"burst_delay: {sum(shot_delay_list) / len(shot_delay_list)}")

    with open("frame_results\\frame_data.json", "w") as f:
        json.dump(out_jdata, f, indent=4)


analyze_video('test.mp4')