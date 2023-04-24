from time import sleep
import mouse

def move_mouse_absolute():
    mouse.move(1200, 700)

def move_mouse_relative():
    mouse.move(200, 200, absolute=False)

def move_mouse_relative_1sec():
    mouse.move(200, 200, absolute=False, duration=1)

sleep(1)
move_mouse_absolute()
sleep(1)
move_mouse_relative()
sleep(1)
move_mouse_relative_1sec()