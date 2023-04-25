# import os
from enum import Enum
import os
from time import sleep
import numpy as np
from mss import mss
from lib import cvar_parser

cvar: cvar_parser.Cvar = cvar_parser.CvarSingleton.get_instance()
SCREEN_WIDTH_PX = int(cvar.graphics.fullscreen_resolution_width)
SCREEN_HEIGHT_PX = int(cvar.graphics.fullscreen_resolution_height)

__bounds = (0, 0, SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX)
if __name__ == "__main__":
    sct = mss()
    from mss import mss
    screenshot = lambda : np.array(sct.grab(__bounds))
else:
    from lib.screen_capture import get_screen_shot
    screenshot = lambda : get_screen_shot(__bounds)


class Location(Enum):
    Javelin = 2
    Cauldron = 3


def run(location: Location):
    if location == Location.Javelin:
        from Stability.locations.javelin import test
    elif location == Location.Cauldron:
        from Stability.locations.cauldron import test
    else:
        raise Exception("Invalid location")
    return test(screenshot)


# if __name__ == "__main__":
#     sleep(3)
#     import sys
#     location = Location[sys.argv[1]]
#     run(location)
