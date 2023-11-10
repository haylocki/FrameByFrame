import json
import os
from Gui_Values import Gui_Values


class Settings:
    def __init__(self, current_dir: str):
        self.current_dir = current_dir
        self.settings_filename = "settings.json"

    def load(self, gui_values: Gui_Values) -> Gui_Values:
        file_path = f"{self.current_dir}/{self.settings_filename}"

        if not os.path.exists(file_path):
            return gui_values

        try:
            with open(file_path, "r") as file:
                settings_dict = json.load(file)
                gui_values.__dict__.update(settings_dict)
        except IOError as e:
            print(f"Error loading settings: {e}")

        return gui_values

    def save(self, gui_values: Gui_Values):
        settings_dict = gui_values.__dict__
        file_path = f"{self.current_dir}/{self.settings_filename}"

        try:
            with open(file_path, "w") as file:
                json.dump(settings_dict, file)
        except IOError as e:
            print(f"Error saving settings: {e}")
