import multiprocessing as mp
import threading as th
import time
from typing import Callable, Optional
from pynput import keyboard as inp

import Reload, Stability, RPM, Cones, Handling
from lib.gui_framework import GuiParent

SUB_PROCESS: Optional[mp.Process] = None
GUI = None

START_KEY = inp.KeyCode(char="[")
END_KEY = inp.KeyCode(char="]")
INFO_KEY = inp.KeyCode(char="i")


def gui_runtime(gui: GuiParent, dict: dict):
    while True:
        if gui.tick(dict):
            break
        print("gui closed")
        time.sleep(1/60)


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

def run(arg):
    print("running")

def run_script(_singleton: dict):
    global SUB_PROCESS
    if not SUB_PROCESS:
        SUB_PROCESS = mp.Process(target=run, args=(_singleton,))
        SUB_PROCESS.start()
        pass


def main():
    global SUB_PROCESS
    global GUI
    GUI = GuiParent(["Stability", "Reload", "RPM", "Cones", "Handling"])
    scripts: dict[str, tuple[Callable, Callable]] = {}
    #for modules in this directory
    for m in [Reload, Stability, RPM, Cones, Handling]:
        try:
            if m.ignore():
                continue
        except AttributeError:
            continue
        func_map: dict[str, tuple[Callable, Callable]] = getattr(m, "FUNC_MAP", {})
        for key in func_map:
            scripts[key] = func_map[key]
    script_idx = 0

    singleton = mp.Manager().dict()
    singleton["script_idx"] = 0
    singleton["result"] = "null"
    lst = inp.Listener(on_press=lambda key: key_press(
        key, singleton))  # type: ignore
    lst.start()
    gui_runtime(GUI, singleton)  # type: ignore
    lst.stop()
    if SUB_PROCESS:
        SUB_PROCESS.kill()
        SUB_PROCESS.terminate()


if __name__ == "__main__":
    main()
