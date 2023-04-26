
from dataclasses import dataclass
from typing import Any, Callable, List
import PySimpleGUI as g
from . import cvar_parser

cvar: cvar_parser.Cvar = cvar_parser.CvarSingleton.get_instance()
SCREEN_WIDTH = int(cvar.graphics.fullscreen_resolution_width)
SCREEN_HEIGHT = int(cvar.graphics.fullscreen_resolution_height)

@dataclass(frozen=True)
class PresetLayout:
    name: str


class GuiParent:
    def __init__(self, name: str, layout: List[List[g.Element]]):
        self.name = name
        self.layout = layout
        self.window = window = g.Window(
            title='Destiny Testing',
            layout=layout,
            size=(SCREEN_WIDTH//8, SCREEN_HEIGHT//8),
            keep_on_top=True,
            finalize=True,
            icon='icon.ico',
            relative_location=((SCREEN_WIDTH//2)-(SCREEN_WIDTH//6.3), (-SCREEN_HEIGHT//2.7)),
            )
        self.scripts: List[Callable[[str, Any], None]] = []

    async def tick(self):
        event, values = self.window.read(timeout=100) # type: ignore
        for func in self.scripts:
            func(event, values)
        if event == g.WIN_CLOSED or event == 'Exit':
            self.close()
        return event, values

    def add_script(self, script: Callable[[str, Any], None]):
        self.scripts.append(script)

    def close(self):
        self.window.close()

class GuiComponent:
    def __init__(self, gui):
        self.gui = gui