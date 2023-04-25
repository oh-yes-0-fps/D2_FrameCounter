
import math
from lib import cvar_parser
from typing import Tuple


cvar: cvar_parser.Cvar = cvar_parser.CvarSingleton.get_instance()
SCREEN_WIDTH_PX = int(cvar.graphics.fullscreen_resolution_width)
SCREEN_HEIGHT_PX = int(cvar.graphics.fullscreen_resolution_height)

def normalize_point(point: tuple[int, int], screen_dimensions: Tuple[int, int]) -> tuple[float, float]:
    return (point[0]/screen_dimensions[0], point[1]/screen_dimensions[1])

def __sub_calc(p1: Tuple[int, int], p2: Tuple[int, int]) -> Tuple[float, float]:
    p1_n = normalize_point(p1, (SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX))
    p2_n = normalize_point(p2, (SCREEN_WIDTH_PX, SCREEN_HEIGHT_PX))
    pc_n = (0.5, 0.5)#normalized center point

    slope = (p2_n[1] - p1_n[1])/(p2_n[0] - p1_n[0])

    rotated_p1_y = p1_n[0]*math.sin(-math.atan(slope))+p1_n[1]*math.cos(-math.atan(slope))
    rotated_p1_x = p1_n[0]*math.cos(math.atan(-slope))-p1_n[1]*math.sin(math.atan(-slope))

    # never used
    # rotated_p2_y = p2_n[0]*math.sin(-math.atan(slope))+p2_n[1]*math.cos(-math.atan(slope))
    rotated_p2_x = p2_n[0]*math.cos(math.atan(-slope))-p2_n[1]*math.sin(math.atan(-slope))

    rotated_pc_y = pc_n[0]*math.sin(-math.atan(slope))+pc_n[1]*math.cos(-math.atan(slope))
    rotated_pc_x = pc_n[0]*math.cos(math.atan(-slope))-pc_n[1]*math.sin(math.atan(-slope))

    yc_shifted = rotated_p1_y-rotated_pc_y
    dixt_x12 = rotated_p2_x-rotated_p1_x
    
    x1_shift = rotated_p1_x-(dixt_x12/2)
    x2_shift = rotated_p2_x-(dixt_x12/2)
    xc_shift = rotated_pc_x-(dixt_x12/2)

    xc_scale = xc_shift/(abs(x2_shift-x1_shift))
    yc_scale = yc_shifted/(abs(x2_shift-x1_shift))

    return (xc_scale, yc_scale)

def calc(data) -> float:
    befor_pair = data[0]
    after_pair = data[1]

    adj_before = __sub_calc(befor_pair[0], befor_pair[1])
    adj_after = __sub_calc(after_pair[0], after_pair[1])

    return math.sqrt((adj_before[0]-adj_after[0])**2+(adj_before[1]-adj_after[1])**2)



