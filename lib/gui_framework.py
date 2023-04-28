
from typing import List, Tuple
import PySimpleGUI as g
from . import cvar_parser

cvar: cvar_parser.Cvar = cvar_parser.CvarSingleton.get_instance()
SCREEN_WIDTH = int(cvar.graphics.fullscreen_resolution_width)
SCREEN_HEIGHT = int(cvar.graphics.fullscreen_resolution_height)

def rollover(length: int, idx: int) -> int:
    if idx >= length:
        return idx % (length-1)
    elif idx < 0:
        if idx < -length:
            return length + (idx % (length-1))
        return length + idx
    else:
        return idx

class GuiParent:
    __CLOSED = False
    __layout = [
        [
            g.Text("Empty", key="l_script", justification="left",
                   enable_events=True),  # size=(SCREEN_WIDTH//32, 1),
            g.Text("Empty", key="c_script", justification="center", text_color="#FFFF00",
                   auto_size_text=True, expand_x=True),  # size=(SCREEN_WIDTH//16, 1),
            g.Text("Empty", key="r_script", justification="right",
                   enable_events=True)  # size=(SCREEN_WIDTH//32, 1),
        ],
        [g.Text("Empty", key="result", size=(
            SCREEN_WIDTH//12, 1), justification="center")],
        [g.Text("", key="error", size=(SCREEN_WIDTH//8, 2),
                background_color="#472b62", text_color="#FF0000", justification="center")],
        [g.Button("Exit")]
    ]

    def __init__(self, scripts: List[str]):
        self.name = "Destiny Testing"
        g.theme('DarkBlue')   # Add a touch of color
        self.window = g.Window(
            title='Destiny Testing',
            layout=self.__layout,
            size=(SCREEN_WIDTH//8, SCREEN_HEIGHT//8),
            keep_on_top=True,
            finalize=True,
            icon='icon.ico',
            # relative_location=((SCREEN_WIDTH//3), (-SCREEN_HEIGHT//2.7)),
            relative_location=((SCREEN_WIDTH//2.31), (-SCREEN_HEIGHT//2.11)),
            background_color="#472b62",
            button_color=("#ffe7d1", "#4b8e8d"),
            element_justification="center",
            alpha_channel=0.7
        )
        g.SetOptions(text_element_background_color="#4b8e8d")
        self.l_script_idx = -1
        self.c_script_idx = 0
        self.r_script_idx = 1
        self.scripts = scripts

    def tick(self, dict: dict):
        update_script_text = False
        if self.__CLOSED:
            return True
        else:
            event, values = self.window.read()  # type: ignore
            print(event, values)
            if event == g.WIN_CLOSED or event == 'Exit' or event == None:
                self.close()
                return True
            if event == "l_script":
                self.c_script_idx = rollover(len(self.scripts), self.c_script_idx-1)
                self.l_script_idx = rollover(len(self.scripts), self.l_script_idx-1)
                self.r_script_idx = rollover(len(self.scripts), self.r_script_idx-1)
                update_script_text = True
            elif event == "r_script":
                self.c_script_idx = rollover(len(self.scripts), self.c_script_idx+1)
                self.l_script_idx = rollover(len(self.scripts), self.l_script_idx+1)
                self.r_script_idx = rollover(len(self.scripts), self.r_script_idx+1)
                update_script_text = True
            if update_script_text:
                self.window["l_script"].update(
                    self.scripts[self.l_script_idx])  # type: ignore
                self.window["c_script"].update(
                    self.scripts[self.c_script_idx])  # type: ignore
                self.window["r_script"].update(
                    self.scripts[self.r_script_idx])  # type: ignore
            try:
                result: str = dict["result"]
                self.window["result"].update(
                    result)  # type: ignore
            except KeyError:
                pass
            try:
                errors: str = dict["error"]
                self.window["error"].update(errors)  # type: ignore
            except KeyError:
                pass
        return False

    def close(self):
        self.window.close()
        self.__CLOSED = True

def is_image_path(txt: str) -> bool:
    return txt.startswith("./")

class GuiComponent:
    def __init__(self, name, gui, text: str):
        self.gui: GuiParent = gui
        self.name = name
        # parse images from text
        # images are formatted like !IMAGE_PATH!
        layout: List[List[g.Element]] = [[g.Text(name, justification="center")]]
        for txt in text.split("!"):
            if is_image_path(txt):
                layout.append([g.Image(filename=txt)])# type: ignore
            else:
                layout.append([g.Multiline(txt, justification="center", text_color="#FFFFFF", expand_x=True, disabled=True)])# type: ignore
        layout.append([g.Button("Exit")])
        self.layout = layout

    def create(self):
        self.window = g.Window(
            title=self.name,
            layout=self.layout,
            size=(SCREEN_WIDTH//3, SCREEN_HEIGHT//3),
            keep_on_top=True,
            modal=True,
            no_titlebar=True,
            grab_anywhere=True,
            finalize=True,
            background_color="#472b62",
            button_color=("#ffe7d1", "#4b8e8d"),
            element_justification="center"
        )

    def close(self):
        self.window.close()


