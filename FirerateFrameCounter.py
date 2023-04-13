from dataclasses import dataclass
import cv2
import numpy as np
import json
import os
import csv

TICK_DURATION = 1/30

FRAME_CAP = 999999999

#can reduce accuracy but allows for low mag red numbers to be counted *somewhat* properly
RED_DETECTION = True

with open("config.json", "r") as f:
    config = json.load(f)
HEIGHT_OFFSET = config["heightOffset"]
WIDTH_OFFSET = config["widthOffset"]

with open("resources\\numbers.json", "r") as f:
    NUMBERS = json.load(f)

#delete all frames in the folder

if not os.path.exists("frame_results"):
    os.mkdir("frame_results")
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

def average(lst: list):
    return sum(lst) / len(lst)

out_jdata = {}
def frameToNumber(frame:np.ndarray, rgb:bool=False) -> int:
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
    return int(max(num_data, key=num_data.get)) #type: ignore


def analyze_video(file_path:str, burst_size: int):
    cap = cv2.VideoCapture(file_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"FPS: {fps}")
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

        #if pixel r > 120 and g < 70 and b < 70 then make it white
        if RED_DETECTION:
            red_threshhold = 80
            frame[:,:,2] = np.where(frame[:,:,2] > red_threshhold, 255, frame[:,:,2]) #type: ignore
            frame[:,:,1] = np.where(frame[:,:,2] > red_threshhold, 255, frame[:,:,1]) #type: ignore
            frame[:,:,0] = np.where(frame[:,:,2] > red_threshhold, 255, frame[:,:,0]) #type: ignore

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
        if frame_num > 1 and num == last_frame-1:
            if shoot_frame_list:
                shot_delay_list.append((frame_num - shoot_frame_list[-1])/fps)
            shoot_frame_list.append(frame_num)
            cv2.imwrite(f"frame_results\\frame_{int(frame_num)}_is_{num}.png", frame_gray)
        last_frame = num
        if frame_num >= FRAME_CAP:
            break

    if burst_size > 1:
        burst_delay_num = []
        inner_burst_delay_num = []
        for i in range(len(shot_delay_list)):
            if (i+1) % burst_size:
                inner_burst_delay_num.append(shot_delay_list[i])
            else:
                dbug = shot_delay_list[i]
                burst_delay_num.append(shot_delay_list[i])

        burst_delay = average(burst_delay_num)
        inner_burst_delay = average(inner_burst_delay_num)
        burst_duration = inner_burst_delay*(burst_size-1)

        bullets_shot = len(shot_delay_list)+1

        bursts = bullets_shot / burst_size

        print(f"burst_delay: {burst_delay} : {burst_delay/TICK_DURATION}")
        print(f"inner_burst_delay: {inner_burst_delay} : {inner_burst_delay/TICK_DURATION}")
        print(f"burst duration: {inner_burst_delay*(burst_size-1)}")
        print(f"RPM: {60 / ((burst_delay+burst_duration)/burst_size)}")
        # print(f"oh_yes_RPM: {60 / ((burst_duration*bursts+burst_delay*(bursts-1))/bullets_shot)}")
        # print(f"rok_RPM?: {60 * ((len(shot_delay_list)+1) / sum(shot_delay_list))}")
    else:
        burst_delay = sum(shot_delay_list) / len(shot_delay_list)
        print(f"burst_delay: {burst_delay} : {burst_delay/TICK_DURATION}")
        print(f"RPM: {60 / ((sum(shot_delay_list) / len(shot_delay_list)))}")

    with open("frame_results\\frame_data.json", "w") as f:
        json.dump(out_jdata, f, indent=4)
    cap.release()

@dataclass()
class RowEntry:
    file: str
    burst_delay: float
    inner_burst_delay: float
    burst_size: int
    burst_delay_ticks: float
    inner_burst_delay_ticks: float
    rpm: float

    def to_string(self):
        return f"{self.file},{self.burst_delay},{self.inner_burst_delay},{self.burst_size},{self.burst_delay_ticks},{self.inner_burst_delay_ticks},{self.rpm}"
    def to_list(self):
        return [self.file, self.burst_delay, self.inner_burst_delay, self.burst_size, self.burst_delay_ticks, self.inner_burst_delay_ticks, self.rpm]

def analyze_video_multi(file_path:str, burst_size: int) -> RowEntry:
    cap = cv2.VideoCapture(file_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"FPS: {fps}")
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

        #if pixel r > 120 and g < 70 and b < 70 then make it white
        if RED_DETECTION:
            red_threshhold = 80
            frame[:,:,2] = np.where(frame[:,:,2] > red_threshhold, 255, frame[:,:,2]) #type: ignore
            frame[:,:,1] = np.where(frame[:,:,2] > red_threshhold, 255, frame[:,:,1]) #type: ignore
            frame[:,:,0] = np.where(frame[:,:,2] > red_threshhold, 255, frame[:,:,0]) #type: ignore

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
        if frame_num > 1 and num == last_frame-1:
            if shoot_frame_list:
                shot_delay_list.append((frame_num - shoot_frame_list[-1])/fps)
            shoot_frame_list.append(frame_num)
            # cv2.imwrite(f"frame_results\\frame_{int(frame_num)}_is_{num}.png", frame_gray)
        last_frame = num
        if frame_num >= FRAME_CAP:
            break
    cap.release()

    if burst_size > 1:
        burst_delay_num = []
        inner_burst_delay_num = []
        for i in range(len(shot_delay_list)):
            if (i+1) % burst_size:
                inner_burst_delay_num.append(shot_delay_list[i])
            else:
                dbug = shot_delay_list[i]
                burst_delay_num.append(shot_delay_list[i])

        burst_delay = average(burst_delay_num)
        inner_burst_delay = average(inner_burst_delay_num)
        burst_duration = inner_burst_delay*(burst_size-1)

        bullets_shot = len(shot_delay_list)+1

        bursts = bullets_shot / burst_size

        rpm = 60 / ((burst_delay+burst_duration)/burst_size)

        return RowEntry(file_path.split('_')[0].split('/')[-1], burst_delay, inner_burst_delay, burst_size, burst_delay/TICK_DURATION, inner_burst_delay/TICK_DURATION, rpm)
    else:
        burst_delay = sum(shot_delay_list) / len(shot_delay_list)
        rpm = 60 / burst_delay
        return RowEntry(file_path.split('_')[0].split('/')[-1], burst_delay, 0, 1, burst_delay/TICK_DURATION, 0, rpm)


SINGLE = True
if SINGLE:
    file_path = "./weapons/prospector_1b.mp4"
    b_size = int(file_path.split('_')[-1].removesuffix('b.mp4'))
    analyze_video(file_path, b_size)
else:
    weapon_data: list[RowEntry] = []
    for file in os.listdir("./weapons"):
        if file.endswith(".mp4"):
            print(f"analyzing {file}")
            b_size = int(file.split('_')[-1].removesuffix('b.mp4'))
            weapon_data.append(analyze_video_multi(f"./weapons/{file}", b_size))
    with open("output.csv", "w") as f:
        import csv
        writer = csv.writer(f)
        writer.writerow(["file", "burst_delay", "inner_burst_delay", "burst_size", "burst_delay_ticks", "inner_burst_delay_ticks", "rpm"])
        for row in weapon_data:
            writer.writerow(row.to_list())

