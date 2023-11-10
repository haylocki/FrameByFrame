import re
from PyQt5.QtCore import QProcess, QObject, pyqtSlot, pyqtSignal
from Gui_Values import Gui_Values


class Ffmpeg_Utils(QObject):
    finished_signal = pyqtSignal()
    progress_callback = pyqtSignal(int)

    def __init__(self, update_progress_callback):
        super().__init__()
        self.subprocess_proc = None
        self.progress_callback.connect(update_progress_callback)

    def run_ffmpeg(
        self,
        gui_values: Gui_Values,
        image_dir: str,
        total_images: int,
        fps: str,
        selected_file: str,
        output_file: str,
    ):
        enhanced_image_dir = f"{image_dir}enhanced/"
        self.total_images = total_images

        ffmpeg_command = [
            "-y",
            "-framerate",
            fps,
            "-i",
            f"{enhanced_image_dir}%06d.png",
            "-i",
            selected_file,
            "-map",
            "0",
            "-map",
            "1:a",
            "-c:a",
            "copy",
            "-c:v",
            "libx265",
            "-crf",
            gui_values.crf,
            "-pix_fmt",
            gui_values.chroma,
            "-preset",
            gui_values.preset,
            output_file,
        ]
        self.subprocess_proc = QProcess(self)
        self.subprocess_proc.readyReadStandardError.connect(self.read_ffmpeg_output)
        self.subprocess_proc.finished.connect(self.encoding_finished)

        try:
            self.subprocess_proc.start("ffmpeg", ffmpeg_command)
        except OSError as e:
            print(f"Error starting ffmpeg process: {e}")

    pyqtSlot()

    def read_ffmpeg_output(self):
        if self.subprocess_proc is None:
            return

        output = self.subprocess_proc.readAllStandardError().data().decode().strip()
        frame_number = self.get_ffmpeg_frame_number(output)
        # percentage for encoding video is 50%-100%
        progress_percentage = int((frame_number / self.total_images) * 50) + 50
        self.progress_callback.emit(progress_percentage)

    @staticmethod
    def get_ffmpeg_frame_number(output: str) -> int:
        frame_match = re.search(r"frame=\s*(\d+)", output)
        frame_number = 0
        if frame_match:
            frame_number = int(frame_match.group(1))

        return frame_number

    def encoding_finished(self):
        self.finished_signal.emit()
