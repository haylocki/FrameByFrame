from dataclasses import dataclass

from Gui_Values import Gui_Values


@dataclass
class Scene:
    start_frame: int
    gui_values: Gui_Values
