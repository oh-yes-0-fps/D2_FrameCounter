from time import sleep
import pynput

def move_mouse_absolute():
    mouse = pynput.mouse.Controller()
    mouse.position = (1200, 700)

def move_mouse_relative():
    mouse = pynput.mouse.Controller()
    mouse.move(200, 200)

sleep(1)
move_mouse_absolute()
sleep(1)
move_mouse_relative()