import cv2
import numpy as np
import time
import mss
import mss.tools
from pynput.mouse import Listener

is_retina = False

def is_clicked(x, y, button, pressed):
    if pressed:
        global start_time
        start_time = time.time()
        return False # to stop the thread after click

def region_grabber(region):
    if is_retina: region = [n * 2 for n in region]
    x1 = region[0]
    y1 = region[1]
    width = region[2]
    height = region[3]

    region = x1, y1, width, height
    with mss.mss() as sct:
        monitor = {"top": y1, "left": x1, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        return sct_img


def imagesearcharea(image, x1, y1, x2, y2, precision=0.8, im=None):
    if im is None:
        im = region_grabber(region=(x1, y1, x2, y2))
        if is_retina:
            im.thumbnail((round(im.size[0] * 0.5), round(im.size[1] * 0.5)))
    img_rgb = np.array(im)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(image, 0)
    if template is None:
        raise FileNotFoundError('Image file not found: {}'.format(image))

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val < precision:
        return [-1, -1]
    return max_loc

def imagesearch_region_loop(image, timesample, x1, y1, x2, y2, precision=0.8):
    with mss.mss() as sct:
        monitor = {"top": y1, "left": x1, "width": x2, "height": y2}
        im = sct.grab(monitor)
    pos = imagesearcharea(image, x1, y1, x2, y2, precision, im)

    while pos[0] == -1:
        with mss.mss() as sct:
            monitor = {"top": y1, "left": x1, "width": x2, "height": y2}
            im = sct.grab(monitor)
        time.sleep(timesample)
        pos = imagesearcharea(image, x1, y1, x2, y2, precision, im)
    return pos

with Listener(on_click=is_clicked) as listener:
    listener.join()

pos = imagesearch_region_loop("overload.png",0.01,136,660,45,45)
if pos[0] != -1:
    end_time = time.time()
    print("{:.3f}".format(end_time-start_time))
else:
    print("image not found")