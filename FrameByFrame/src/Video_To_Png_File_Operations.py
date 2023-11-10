import cv2
import numpy as np
import os
import shutil
from Dialogs import Dialogs
from PyQt5.QtWidgets import QMainWindow


class Video_To_Png_File_Operations:
    def __init__(self):
        self.frame_width = 0
        self.frame_height = 0

    def frame_size(self, video: cv2.VideoCapture) -> None:
        self.frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def read_frame(self, video: np.ndarray, image_counter: int) -> np.ndarray:
        success, image = video.read()
        if not success:
            print(f"Error reading frame {image_counter}")
            image = np.zeros((self.frame_height, self.frame_width, 3), dtype=np.uint8)

        return image

    @staticmethod
    def delete_ssim_values(image_dir: str):
        file_path = f"{image_dir}ssim_values.txt"
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing file {file_path}: {e}")

    @staticmethod
    def open_video(selected_file: str) -> cv2.VideoCapture:
        video = cv2.VideoCapture(selected_file)

        if not video.isOpened():
            print("Error opening video file")
            return None

        return video

    @staticmethod
    def total_images(video: cv2.VideoCapture) -> int:
        return int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    @staticmethod
    def write_frame(output_file: str, image: cv2.VideoCapture):
        try:
            # Save the image as a png image
            cv2.imwrite(output_file, image)
        except Exception as e:
            print(f"Error saving image {output_file}: {e}")

    @staticmethod
    def check_for_png(window: QMainWindow, image_dir: str) -> bool:
        result = True

        if any(f.endswith(".png") for f in os.listdir(image_dir)):
            if Dialogs.overwrite_dialog(window):
                try:
                    if os.path.exists(image_dir):
                        shutil.rmtree(image_dir)
                        os.makedirs(image_dir)
                except Exception as e:
                    print(f"Error creating image directory: {e}")
            else:
                result = False

        return result
