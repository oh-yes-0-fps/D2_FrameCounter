# import os
import keyboard
import math
import os
from time import sleep
from mss import mss
import numpy as np
import cv2
import pyautogui
import mouse

sct = mss()

with open("config.json", "r") as f:
    import json
    config = json.load(f)
    SCREEN_WIDTH_PX = config["screenWidth"]
    SCREEN_HEIGHT_PX = config["screenHeight"]

class MovingAveragePoint:
    def __init__(self, entries) -> None:
        self.entries = entries
        self.points = []

    def add_point(self, point):
        self.points.append(point)
        if len(self.points) > self.entries:
            self.points.pop(0)
    
    def get_average(self):
        return (sum([x[0] for x in self.points])/len(self.points), sum([x[1] for x in self.points])/len(self.points))

    def get_average_int(self):
        return (int(sum([x[0] for x in self.points])/len(self.points)), int(sum([x[1] for x in self.points])/len(self.points)))

    def debounce(self, point):
        if abs(point[0] - self.points[-1][0]) < 0.01 and abs(point[1] - self.points[-1][1]) < 0.01:
            return True
        return False

    def clear(self):
        self.points = []

    def samples(self):
        return len(self.points)

def sort_points(keypoints) -> tuple:
    points = []
    for point in keypoints:
        points.append((point.pt[0], point.pt[1]))
    points.sort(key=lambda x: x[0])
    return tuple(points)

def point_pos_cauld(debug = False):
    screen = np.array(sct.grab((0, 0, SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX)))
    screen[screen[:, :, 0] < 230] = [0, 0, 0, 0]
    screen[screen[:, :, 2] < 230] = [0, 0, 0, 0]
    screen[screen[:, :, 1] < 230] = [0, 0, 0, 0]

    screen[screen[:, :, 0] > 20] = [255, 255, 255, 255]
    screen[screen[:, :, 2] > 20] = [255, 255, 255, 255]
    screen[screen[:, :, 1] > 20] = [255, 255, 255, 255]

    #detect white rectangular blobs
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 1
    params.maxArea = 2500
    params.filterByCircularity = False
    # params.minCircularity = 0.5
    # params.maxCircularity = 100
    params.filterByConvexity = False
    params.filterByInertia = False
    params.filterByColor = True
    params.blobColor = 255
    params.minDistBetweenBlobs = 100

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(screen)

    if debug:
        im_with_keypoints = cv2.drawKeypoints(screen, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        im_with_keypoints = cv2.resize(im_with_keypoints, (int(SCREEN_WIDTH_PX/3), int(SCREEN_HEIGHT_PX/3)))
        cv2.imshow("Keypoints", im_with_keypoints)
        cv2.waitKey(1)

    return sort_points(keypoints)

def point_pos_jav(debug = False):
    screen = np.array(sct.grab((0, 0, SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX)))
    screen[screen[:, :, 0] < 245] = [0, 0, 0, 0]
    screen[screen[:, :, 2] < 175] = [0, 0, 0, 0]
    screen[screen[:, :, 1] < 180] = [0, 0, 0, 0]

    screen[screen[:, :, 0] > 20] = [255, 255, 255, 255]
    screen[screen[:, :, 2] > 20] = [255, 255, 255, 255]
    screen[screen[:, :, 1] > 20] = [255, 255, 255, 255]

    #detect white rectangular blobs
    params = cv2.SimpleBlobDetector_Params()
    params.filterByArea = True
    params.minArea = 100
    params.maxArea = 2500
    params.filterByCircularity = False
    # params.minCircularity = 0.5
    # params.maxCircularity = 100
    params.filterByConvexity = False
    params.filterByInertia = False
    params.filterByColor = True
    params.blobColor = 255
    params.minDistBetweenBlobs = screen.shape[1]//5

    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(screen)

    if debug:
        im_with_keypoints = cv2.drawKeypoints(screen, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        im_with_keypoints = cv2.resize(im_with_keypoints, (int(SCREEN_WIDTH_PX/3), int(SCREEN_HEIGHT_PX/3)))
        cv2.imshow("Keypoints", im_with_keypoints)
        cv2.waitKey(1)

    return sort_points(keypoints)

def normalize_point(point: tuple[int, int]) -> tuple[float, float]:
    return (point[0]/SCREEN_WIDTH_PX, point[1]/SCREEN_HEIGHT_PX)






def test_3():
    moving_average_1 = MovingAveragePoint(5)
    moving_average_2 = MovingAveragePoint(5)
    moving_average_3 = MovingAveragePoint(5)
    while moving_average_1.samples() < 5:
        sleep(0.1)
        points = point_pos_cauld()
        if len(points) < 3:
            print("not enough points")
            sleep(0.1)
            continue
        moving_average_1.add_point(points[0])
        moving_average_2.add_point(points[1])
        moving_average_3.add_point(points[2])
    print(
        moving_average_1.get_average_int(),
        moving_average_2.get_average_int(),
        moving_average_3.get_average_int()
    )
    moving_average_1.clear()
    moving_average_2.clear()
    moving_average_3.clear()
    mouse.press(button="left")
    sleep(.5)
    mouse.release(button="left")
    for i in range(5):
        sleep(0.1)
        points = point_pos_cauld()
        if len(points) < 3:
            print("not enough points")
            continue
        moving_average_1.add_point(points[0])
        moving_average_2.add_point(points[1])
        moving_average_3.add_point(points[2])
    def debouce(ma_1: MovingAveragePoint, ma_2: MovingAveragePoint, ma_3: MovingAveragePoint):
        out = True
        points = point_pos_cauld()
        if len(points) < 3:
            print("not enough points")
            return False
        if not ma_1.debounce(points[0]):
            out = False
        if not ma_2.debounce(points[1]):
            out = False
        if not ma_3.debounce(points[2]):
            out = False
        return out
    while not debouce(moving_average_1, moving_average_2, moving_average_3):
        sleep(0.1)
        points = point_pos_cauld(True)
        if len(points) < 3:
            print("not enough points")
            continue
        moving_average_1.add_point(points[0])
        moving_average_2.add_point(points[1])
        moving_average_3.add_point(points[2])
    print(
        moving_average_1.get_average_int(),
        moving_average_2.get_average_int(),
        moving_average_3.get_average_int()
    )

def test_jav():
    moving_average_1 = MovingAveragePoint(5)
    moving_average_2 = MovingAveragePoint(5)
    while moving_average_1.samples() < 5:
        sleep(0.1)
        points = point_pos_jav()
        if len(points) < 2:
            print("not enough points")
            sleep(0.1)
            continue
        moving_average_1.add_point(points[0])
        moving_average_2.add_point(points[1])
    print(
        moving_average_1.get_average_int(),
        moving_average_2.get_average_int(),
    )
    moving_average_1.clear()
    moving_average_2.clear()
    mouse.press(button="left")
    sleep(.5)
    mouse.release(button="left")
    for i in range(5):
        sleep(0.1)
        points = point_pos_jav()
        if len(points) < 2:
            print("not enough points")
            continue
        moving_average_1.add_point(points[0])
        moving_average_2.add_point(points[1])
    def debouce(ma_1: MovingAveragePoint, ma_2: MovingAveragePoint):
        out = True
        points = point_pos_jav()
        if len(points) < 2:
            print("not enough points")
            return False
        if not ma_1.debounce(points[0]):
            out = False
        if not ma_2.debounce(points[1]):
            out = False
        return out
    while not debouce(moving_average_1, moving_average_2):
        sleep(0.1)
        points = point_pos_jav(True)
        if len(points) < 2:
            print("not enough points")
            continue
        moving_average_1.add_point(points[0])
        moving_average_2.add_point(points[1])
    print(
        moving_average_1.get_average_int(),
        moving_average_2.get_average_int(),
    )

sleep(3)
test_jav()





