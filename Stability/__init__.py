
from time import sleep

from Stability.calculator import calc
from Stability import stab_test as test

def ignore():
    return False

def __recoil_func(_dict):
    sleep(1)
    _dict["result"] = ""
    _dict["error"] = ""
    try:
        _dict["result"] = str(calc(test.run(test.Location.Javelin)))
    except Exception as e:
        _dict["error"] = str(e)
    return

FUNC_MAP = {
    "Stability": __recoil_func,
}