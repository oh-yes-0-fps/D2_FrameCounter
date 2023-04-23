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


def debug_screen():
    screen = np.array(sct.grab((0, 0, SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX)))
    screen[screen[:, :, 0] < 248] = [0, 0, 0, 0]
    screen[screen[:, :, 2] < 150] = [0, 0, 0, 0]
    screen[screen[:, :, 1] < 150] = [0, 0, 0, 0]
    # make a red cross across the screen
    screen[screen.shape[0]//2-5:screen.shape[0]//2+5, :, :] = [0, 0, 255, 255]
    screen[:, screen.shape[1]//2-5:screen.shape[1]//2+5, :] = [0, 0, 255, 255]

    cv2.imshow("screen", screen)
    cv2.waitKey(0)


with open("config.json", "r") as f:
    import json
    config = json.load(f)
    SCREEN_WIDTH_PX = config["screenWidth"]
    SCREEN_HEIGHT_PX = config["screenHeight"]

    # start_bind = config["start_bind"]
    # end_bind = config["end_bind"]


def normalize_point(point: tuple[int, int]) -> tuple[float, float]:
    return (point[0]/SCREEN_WIDTH_PX, point[1]/SCREEN_HEIGHT_PX)


def get_point_pos() -> tuple[tuple[int, int], tuple[int, int]]:
    # capture screen 0
    screen = np.array(sct.grab((0, 0, SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX)))

    og_screen = screen.copy()

    # split screen into quarters
    tl_qt = screen[:screen.shape[0]//2, :screen.shape[1]//2]
    tr_qt = screen[:screen.shape[0]//2, screen.shape[1]//2:]

    def get_light_center(qt: np.ndarray, offset: tuple[int, int]):
        # screen goes array[y, x, color]
        try:
            qt_c = qt.copy()
            qt_c[qt_c[:, :, 0] < 248] = [0, 0, 0, 0]
            qt_c[qt_c[:, :, 2] < 150] = [0, 0, 0, 0]
            qt_c[qt_c[:, :, 1] < 150] = [0, 0, 0, 0]
            # move down the screen until the row has blue pixels
            y = 0
            while np.all(qt_c[y, :, :] == [0, 0, 0, 0]):
                y += 1
            # move up the screen until the row has blue pixels
            y2 = min(y + qt_c.shape[0]//10, qt_c.shape[0]-1)
            while np.all(qt_c[y2, :, :] == [0, 0, 0, 0]):
                y2 -= 1
        except:
            quadrant = ""
            if offset == (0, 0):
                quadrant = "top left"
            elif offset == (screen.shape[1]//2, 0):
                quadrant = "top right"
            elif offset == (0, screen.shape[0]//2):
                quadrant = "bottom left"
            elif offset == (screen.shape[1]//2, screen.shape[0]//2):
                quadrant = "bottom right"
            print(f"Error in {quadrant} quadrant for y")
            debug_screen()
            return offset

        try:
            qt_c = qt.copy()
            qt_c[qt_c[:, :, 0] < 248] = [0, 0, 0, 0]
            qt_c[qt_c[:, :, 2] < 150] = [0, 0, 0, 0]
            qt_c[qt_c[:, :, 1] < 150] = [0, 0, 0, 0]
            # move right until the column has blue pixels
            x = 0
            while np.all(qt_c[:, x, :] == [0, 0, 0, 0]):
                x += 1
            # move left until the column has blue pixels
            x2 = min(x + qt_c.shape[0]//5, qt_c.shape[1]-1)
            while np.all(qt_c[:, x2, :] == [0, 0, 0, 0]) or np.all(qt_c[:, min(x2+5, qt_c.shape[1]-1), :] == [0, 0, 0, 0]):
                x2 -= 1
        except:
            quadrant = ""
            if offset == (0, 0):
                quadrant = "top left"
            elif offset == (screen.shape[1]//2, 0):
                quadrant = "top right"
            elif offset == (0, screen.shape[0]//2):
                quadrant = "bottom left"
            elif offset == (screen.shape[1]//2, screen.shape[0]//2):
                quadrant = "bottom right"
            print(f"Error in {quadrant} quadrant for x")
            debug_screen()
            return offset

        # return the center of the blue pixels
        return offset[0]+(x + x2)//2, offset[1]+(y + y2)//2

    tl_x, tl_y = get_light_center(tl_qt, (0, 0))
    tr_x, tr_y = get_light_center(tr_qt, (screen.shape[1]//2, 0))

    tl_point = (tl_x, tl_y)
    tr_point = (tr_x, tr_y)
    # cn_point = (screen.shape[1]//2, screen.shape[0]//2)
    return tl_point, tr_point


def mouse_lineup():
    points = get_point_pos()
    while abs(points[0][1] - points[1][1]) > SCREEN_HEIGHT_PX//200:
        print(abs(points[0][1] - points[1][1]))
        if points[0][1] > points[1][1]:
            print("mouse right")
            sleep(0.1)
        elif points[0][1] < points[1][1]:
            print("mouse left")
            sleep(0.1)
        else:
            print("done")
            break
        points = get_point_pos()
        # clear terminal
        # os.system("cls")


def strafe_lineup():
    diff = 100
    while abs(diff) > SCREEN_WIDTH_PX//200:
        tl_point, tr_point = get_point_pos()
        tl_x = SCREEN_WIDTH_PX//2-tl_point[0]
        tr_x = tr_point[0]-SCREEN_WIDTH_PX//2
        diff = tl_x-tr_x
        os.system("cls")
        print(tl_point, tr_point)
        if diff < 0:
            keyboard.press("d")
            sleep(0.80*(abs(diff)/SCREEN_WIDTH_PX)+0.03)
            keyboard.release("d")
        elif diff > 0:
            keyboard.press("a")
            sleep(0.80*(abs(diff)/SCREEN_WIDTH_PX)+0.03)
            keyboard.release("a")
        else:
            break


def forward_lineup():
    diff = 100
    wanted_y = SCREEN_HEIGHT_PX//2-SCREEN_HEIGHT_PX//15
    while abs(diff) > SCREEN_HEIGHT_PX//200:
        tl_point, tr_point = get_point_pos()
        os.system("cls")
        print(tl_point, tr_point)
        y = int(tl_point[1] + tr_point[1])//2
        diff = y - wanted_y
        if diff < 0:
            keyboard.press("s")
            sleep(0.60*(abs(diff)/SCREEN_HEIGHT_PX)+0.02)
            keyboard.release("s")
        elif diff > 0:
            keyboard.press("w")
            sleep(0.60*(abs(diff)/SCREEN_HEIGHT_PX)+0.02)
            keyboard.release("w")
        else:
            break


def get_triangle_theta():
    tl_point, tr_point = get_point_pos()
    cn_point = (SCREEN_WIDTH_PX//2, SCREEN_HEIGHT_PX//2)

    # adjusts for left and right error
    tl_x = SCREEN_WIDTH_PX//2-tl_point[0]
    tr_x = tr_point[0]-SCREEN_WIDTH_PX//2
    x = (tl_x-tr_x)
    cn_point = (SCREEN_WIDTH_PX//2-x, SCREEN_HEIGHT_PX//2)

    # point 1 is the top left point
    # point 2 is the center point
    # point 3 is the top right point
    # get angle of points 1->2->3
    dist_1_2 = np.sqrt((tl_point[0]-cn_point[0]) **
                       2 + (tl_point[1]-cn_point[1])**2)
    dist_2_3 = np.sqrt((tr_point[0]-cn_point[0]) **
                       2 + (tr_point[1]-cn_point[1])**2)
    dist_1_3 = np.sqrt((tl_point[0]-tr_point[0]) **
                       2 + (tl_point[1]-tr_point[1])**2)
    theta = np.arccos((dist_1_2**2 + dist_2_3**2 -
                      dist_1_3**2)/(2*dist_1_2*dist_2_3))
    theta = np.degrees(theta)
    return theta


# try:
#     mouse_lineup()
#     strafe_lineup()
#     forward_lineup()
# except:
#     debug_screen()


def test():
    try:
        mouse_lineup()
        strafe_lineup()
        forward_lineup()
    except:
        debug_screen()
    start = get_triangle_theta()
    # hold mouse left for 2/3 second
    mouse.press(button="left")
    sleep(.5)
    mouse.release(button="left")
    sleep(1)
    end = get_triangle_theta()
    print(start-end)
test()


# sleep(3)
# test()
# while True:
#     print(get_point_pos())
