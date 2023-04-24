from mss import mss
import numpy as np
__mss = mss()
def get_screen_shot(bounds) -> np.ndarray:
    return np.array(__mss.grab(bounds))