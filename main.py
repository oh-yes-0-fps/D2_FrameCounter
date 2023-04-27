import multiprocessing as mp
import threading as th
import time
from typing import Optional
import PySimpleGUI as sg
from pynput import keyboard as inp

from Stability import gui_comp as stability_gui
from Reload import gui_comp as reload_gui
from lib.gui_framework import GuiParent

scripts = ["Stability", "Reload", "RPM", "Handling", "AA"]
c_script_idx = 0

SUB_PROCESS: Optional[mp.Process] = None

START_KEY = inp.KeyCode(char="[")
END_KEY = inp.KeyCode(char="]")


def gui_runtime(gui: GuiParent, dict: dict):
    while True:
        if gui.tick(dict):
            break


def key_press(key, _singleton: dict):
    global SUB_PROCESS
    if SUB_PROCESS:
        if not SUB_PROCESS.is_alive():
            SUB_PROCESS.kill()
            SUB_PROCESS.terminate()
    if key == START_KEY and SUB_PROCESS is None:
        run_script(_singleton)
    elif key == END_KEY and SUB_PROCESS is not None:
        SUB_PROCESS.kill()
        SUB_PROCESS.terminate()
        SUB_PROCESS = None


def run_script(_singleton: dict):
    global SUB_PROCESS
    if not SUB_PROCESS:
        SUB_PROCESS = mp.Process(target=run, args=(_singleton,))
        SUB_PROCESS.start()


def main():
    global SUB_PROCESS
    singleton = mp.Manager().dict()
    singleton["script_idx"] = 0
    singleton["instructions"] = "None"
    lst = inp.Listener(on_press=lambda key: key_press(
        key, singleton))  # type: ignore
    lst.start()
    gui_runtime(GuiParent(scripts), singleton)  # type: ignore
    if SUB_PROCESS:
        SUB_PROCESS.kill()
        SUB_PROCESS.terminate()


if __name__ == "__main__":
    main()
