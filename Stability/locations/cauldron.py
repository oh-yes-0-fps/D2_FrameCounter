import cv2
import numpy as np
from time import sleep
from Stability.locations.resources import *
from typing import Callable, List, Tuple
import mouse

def __point_pos(screen: np.ndarray, debug = False):
    if len(screen.shape) < 3:
        raise Exception("Screen matrix is not formatted correctly")
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
        im_with_keypoints = cv2.resize(im_with_keypoints, (1280, 720))
        cv2.imshow("Keypoints", im_with_keypoints)
        cv2.waitKey(1)

    return sort_points(keypoints)


def test(screen_grabber: Callable[[], np.ndarray]) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    out = []
    moving_average_1 = MovingAveragePoint(5)
    moving_average_2 = MovingAveragePoint(5)
    moving_average_3 = MovingAveragePoint(5)
    while moving_average_1.samples() < 5:
        sleep(0.1)
        points = __point_pos(screen_grabber())
        if len(points) < 3:
            print("not enough points")
            sleep(0.1)
            continue
        moving_average_1.add_point(points[0])
        moving_average_2.add_point(points[1])
        moving_average_3.add_point(points[2])
    out.append([
        moving_average_1.get_average_int(),
        moving_average_2.get_average_int(),
        moving_average_3.get_average_int()
    ])
    moving_average_1.clear()
    moving_average_2.clear()
    moving_average_3.clear()
    mouse.press(button="left")
    sleep(.5)
    mouse.release(button="left")
    for i in range(5):
        sleep(0.1)
        points = __point_pos(screen_grabber())
        if len(points) < 3:
            print("not enough points")
            continue
        moving_average_1.add_point(points[0])
        moving_average_2.add_point(points[1])
        moving_average_3.add_point(points[2])
    def debouce(ma_1: MovingAveragePoint, ma_2: MovingAveragePoint, ma_3: MovingAveragePoint):
        out = True
        points = __point_pos(screen_grabber())
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
        points = __point_pos(screen_grabber())
        if len(points) < 3:
            print("not enough points")
            continue
        moving_average_1.add_point(points[0])
        moving_average_2.add_point(points[1])
        moving_average_3.add_point(points[2])
    out.append([
        moving_average_1.get_average_int(),
        moving_average_2.get_average_int(),
        moving_average_3.get_average_int()
    ])
    out = tuple(out)
    if verify_points(out):
        return out
    else:
        raise Exception("points not verified")