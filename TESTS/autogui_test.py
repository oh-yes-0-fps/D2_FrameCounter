from time import sleep
import pyautogui

def move_mouse_absolute():
    pyautogui.moveTo(1200, 700)

def move_mouse_relative():
    pyautogui.moveRel(200, 200)

def move_mouse_relative_1sec():
    pyautogui.moveRel(200, 200, duration=1)

sleep(1)
move_mouse_absolute()
sleep(1)
move_mouse_relative()
sleep(1)
move_mouse_relative_1sec()