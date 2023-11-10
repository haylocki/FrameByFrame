import os
import shutil
from Dialogs import Dialogs
from PyQt5.QtWidgets import QMainWindow


class Enhanced_File_Operations:
    def __init__(self, enhanced_dir: str):
        self.enhanced_dir = enhanced_dir

    def remove(self, window: QMainWindow):
        try:
            if os.path.exists(self.enhanced_dir) and os.listdir(self.enhanced_dir):
                if Dialogs.overwrite_dialog(window):
                    shutil.rmtree(self.enhanced_dir)
        except OSError as e:
            print("here")
            print(f"Error removing enhanced directory: {e}")

    def create(self):
        try:
            if not os.path.exists(self.enhanced_dir):
                os.makedirs(self.enhanced_dir, exist_ok=True)
        except OSError as e:
            print(f"Error creating enhanced directory: {e}")
