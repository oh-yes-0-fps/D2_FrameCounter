import numpy as np
import tensorflow as tf
from tensorflow import keras
import keyboard
from mss import mss
FILE_NAME = 'models/ar_aa'
RENDER_RESOLUTION = 200
SCREEN_HEIGHT_PX = 2160
SCREEN_WIDTH_PX = 3840
BIND = "]"


# HORIZONTAL = True  # if false will use vertical

# pixle offset from the middle most pixel of the axis
PIXEL_OFFSET = 0

DESIRED_COLOR = "G"


ASPECT_RATIO = SCREEN_WIDTH_PX/SCREEN_HEIGHT_PX
PERCENT_FROM_CENTER_OF_SCREEN = 0.1


x_scl = PERCENT_FROM_CENTER_OF_SCREEN/2.0
y_scl = min((PERCENT_FROM_CENTER_OF_SCREEN/2.0)*ASPECT_RATIO, SCREEN_HEIGHT_PX)
crosshair_bounds = (int(SCREEN_WIDTH_PX*(0.5-x_scl)), int(SCREEN_HEIGHT_PX*(0.5-y_scl)),
                    int(SCREEN_WIDTH_PX*(0.5+x_scl)), int(SCREEN_HEIGHT_PX*(0.5+y_scl)))

sct = mss()

def get_verticle_in_matrix(matrix: np.ndarray, pixel_offset: int):
    return matrix[:, matrix.shape[1]//2 + pixel_offset]


def get_horizontal_in_matrix(matrix: np.ndarray, pixel_offset: int):
    return matrix[matrix.shape[0]//2 + pixel_offset, :]


def get_color_from_pixel_array(pixel_matrix: np.ndarray, color_idx: int):
    return pixel_matrix[:, color_idx]


def get_first_half_of_matrix(array: np.ndarray):
    return array[:array.shape[0]//2]

def rgb_idx():
    if DESIRED_COLOR == "R":
        return 2
    elif DESIRED_COLOR == "G":
        return 1
    elif DESIRED_COLOR == "B":
        return 0
    else:
        raise Exception("Invalid desired color")

def get_normalized_reticle_shading(matrix: np.ndarray, horizontal: bool):
    # get the 4 corners of the matrix and average the colors
    tl = matrix[0, 0]
    tr = matrix[0, matrix.shape[1]-1]
    bl = matrix[matrix.shape[0]-1, 0]
    br = matrix[matrix.shape[0]-1, matrix.shape[1]-1]
    bg_avg = np.average([tl, tr, bl, br], axis=0)
    background_color = bg_avg[rgb_idx()]

    #if background_color > 0:
    #    raise Exception("Background is too bright")

    if horizontal:
        _1d_matrix = get_horizontal_in_matrix(matrix, PIXEL_OFFSET)
    else:
        _1d_matrix = get_verticle_in_matrix(matrix, PIXEL_OFFSET)
    pixel_map = get_first_half_of_matrix(_1d_matrix)
    color_map = list(get_color_from_pixel_array(pixel_map, rgb_idx()))
    color_map = [max(x-background_color, 0.0) for x in color_map]
    max_val = max(color_map)
    if max_val == 0:
        return color_map
    full_screen_range = SCREEN_WIDTH_PX/2
    color_map = [(x/max_val, (len(color_map) - i)/full_screen_range)
                 for i, x in enumerate(color_map)]
    return list(color_map)


def get_screenshot() -> np.ndarray:
    return np.array(sct.grab(crosshair_bounds)) # type: ignore

model: tf.keras.Sequential = tf.keras.models.load_model(FILE_NAME) # type: ignore

while True:
    if keyboard.is_pressed(BIND):
        buffer = []
        try:
            for x in get_normalized_reticle_shading(get_screenshot(), True):
                buffer.append(x[0])
        except Exception as e:
            print(e)
            continue
# Generate a new numpy array of integers for prediction
        X_test = np.array(buffer) # Input array of shape (3, 192)
#X_test = np.random.randint(0, 100, size=(3, 192), dtype=np.int32)  # Input array of shape (3, 192)

# Predict using the trained model

        y_pred = model.predict(np.expand_dims(X_test,axis=0))

# Print the predicted values
        print("\nPrediction: {}".format( np.round(y_pred).astype(int)))