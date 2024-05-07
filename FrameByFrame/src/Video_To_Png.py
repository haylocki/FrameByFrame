from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import QObject, pyqtSignal
from Video_To_Png_File_Operations import Video_To_Png_File_Operations
import cv2

class Video_To_Png(QObject):
    progress_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def convert_video_to_png(
        self,
        image_dir: str,
        window: QMainWindow,
        selected_file: str,
    ) -> int:
        file_ops = Video_To_Png_File_Operations()
        total_images = 0

        video = file_ops.open_video(selected_file)

        if video is not None:
            total_images = file_ops.total_images(video)
            file_ops.frame_size(video)

            if file_ops.check_for_png(window, image_dir):
                for image_counter in range(1, total_images + 1):
                    output_file = f"{image_dir}{image_counter:06d}.png"
                    image = file_ops.read_frame(video, image_counter)
                    file_ops.write_frame(output_file, image)
                    progress_percentage = int((image_counter / total_images) * 100)
                    self.progress_signal.emit(progress_percentage)

            file_ops.delete_ssim_values(image_dir)
            video.release()

        return total_images - 1
