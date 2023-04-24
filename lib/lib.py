
from enum import Enum
from typing import Tuple, Union

class ColorFormat(Enum):
    RGB = (0, 1, 2)
    RGBA = (0, 1, 2, 3)
    BGR = (2, 1, 0)
    BGRA = (2, 1, 0, 3)

class Color:
    @staticmethod
    def from_rgb(r: int, g: int, b: int) -> 'Color':
        return Color((r, g, b), ColorFormat.RGB)

    def __init__(self, color: Union[Tuple[int, int, int], Tuple[int, int, int, int]], format: ColorFormat) -> None:
        if len(color) != len(format.value):
            raise ValueError("color and format must have the same number of elements")
        self.color = color
        self.format = format

    @property
    def r(self) -> int:
        return int(self.color[self.format.value[0]])

    @property
    def g(self) -> int:
        return int(self.color[self.format.value[1]])

    @property
    def b(self) -> int:
        return int(self.color[self.format.value[2]])

    @property
    def a(self) -> int:
        try:
            return int(self.color[self.format.value[3]])
        except IndexError:
            raise ValueError("color format does not have an alpha channel")


def crosshair_bounds(percent_of_screen: float, aspect_ratio: float):
    """
    Percent of screen is how big the x of the crosshair is, aspect ratio is how big the y is compared to x \n
    Square is 1/1, 16:9 is 16/9
    """
    pass
