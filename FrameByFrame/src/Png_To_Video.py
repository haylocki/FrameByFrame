import cv2
import os

from Create_Enhanced_Pngs import Enhanced_Png_Creator as cep
from Dialogs import Dialogs
from Ffmpeg_Utils import Ffmpeg_Utils
from Gui_Values import Gui_Values
from Ssim import Ssim
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow


class Png_To_Video(QObject):
    encoding_finished = pyqtSignal()
    finished_signal = pyqtSignal()
    progress_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.cep = cep(self.progress_signal.emit)
        self.dialogs = Dialogs()
        self.cep.processing_finished.connect(self.run_ffmpeg)
        self.ffmpeg_utils = Ffmpeg_Utils(self.progress_signal.emit)
        self.ffmpeg_utils.finished_signal.connect(self.encoding_finished)

    def convert_png_to_video(
        self,
        gui_values: Gui_Values,
        dialogs: Dialogs,
        image_dir: str,
        current_dir: str,
        total_images: int,
        ssim: Ssim,
        window: QMainWindow,
    ):
        self.gui_values = gui_values
        self.image_dir = image_dir
        self.total_images = total_images
        result = False
        self.selected_file = dialogs.open_file_dialog("Select original video file")
        if self.selected_file:
            result = True
            file_no_extn, file_extn = os.path.splitext(self.selected_file)
            self.output_file = file_no_extn + "_new" + file_extn
            video = cv2.VideoCapture(self.selected_file)

            if not video.isOpened():
                print("Error opening original video file")
                return False

            self.fps = "0.0"
            self.fps = str(video.get(cv2.CAP_PROP_FPS))
            
            if self.fps == "0.0":
                print ("Failed to read FPS from file")

            self.cep.create_enhanced_pngs(
                gui_values, image_dir, current_dir, total_images, ssim, window
            )

        return result

    def run_ffmpeg(self):
        self.ffmpeg_utils.run_ffmpeg(
            self.gui_values,
            self.image_dir,
            self.total_images,
            self.fps,
            self.selected_file,
            self.output_file,
        )

    def encoding_finished(self):
        self.dialogs.encoding_finished_dialog()
        self.finished_signal.emit()
