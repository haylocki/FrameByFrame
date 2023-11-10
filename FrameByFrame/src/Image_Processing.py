import os
import shutil
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal

from Image import Image
from Model_Pb import Model_Pb
from Model_SRVGGNetCompact_Pth import Model_SRVGGNetCompact_Pth
from Model_Rrdbnet_Pth import Model_Rrdbnet_Pth

IDENTICAL = 1.0
MULTIPLE_SCALES = False
SINGLE_SCALE = True


class Image_Processing_Worker_Signals(QObject):
    finished = pyqtSignal()


class Image_Processing_Worker(QRunnable):
    def __init__(
        self,
        start_image_index,
        end_image_index,
        enhanced_dir,
        gui_values,
        ssim,
        image_dir,
        current_dir,
        total_images,
        parent=None,
        progress_callback=None,
    ):
        super(Image_Processing_Worker, self).__init__()
        self.signals = Image_Processing_Worker_Signals()
        self.gui_values = gui_values
        self.current_dir = current_dir
        self.image_dir = image_dir
        self.enhanced_dir = enhanced_dir
        self.start_image_index = start_image_index
        self.end_image_index = end_image_index
        self.ssim = ssim
        self.image_dir = image_dir
        self.total_images = total_images
        self.parent = parent
        self.progress_callback = progress_callback

    def count_files(self, directory: str) -> int:
        count = 0
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file():
                    count += 1

        return count

    def setup_model(self, model, single_scale: bool) -> None:
        self.scale_model = model
        self.scale_model.set_single_scale(single_scale)
        self.scale_model.set_scaling_model(self.gui_values.scaling, self.current_dir)
        self.scale_model.create_model()

    def run(self):
        # TensorFlow models
        if (
            self.gui_values.scaling[:4] == "fsrc"
            or self.gui_values.scaling[:4] == "edsr"
        ):
            self.scale_model = Model_Pb()
            self.scale_model.set_scaling_model(
                self.gui_values.scaling, self.current_dir
            )

        # pytorch models
        elif (
            self.gui_values.scaling[4:11] == "AnimeV3"
            or self.gui_values.scaling[:4] == "rybu"
        ):
            self.setup_model(Model_SRVGGNetCompact_Pth(), SINGLE_SCALE)

        elif self.gui_values.scaling[4:10] == "ESRGAN":
            self.setup_model(Model_Rrdbnet_Pth(), MULTIPLE_SCALES)

        elif (
            self.gui_values.scaling[4:11] == "Anime6B"
            or self.gui_values.scaling[:10] == "UltraSharp"
        ):
            self.setup_model(Model_Rrdbnet_Pth(), SINGLE_SCALE)

        self.image = Image(None, None)
        white_balance = self.gui_values.white_balance
        enable_enhancement = self.gui_values.enable_enhancement

        for image_counter in range(self.start_image_index, self.end_image_index):
            # Percentage for frame enhancing is 0%-50%
            progress_percentage = (
                self.count_files(self.enhanced_dir) * 50
            ) // self.total_images
            self.progress_callback.emit(progress_percentage)
            prev_file_path = f"{self.enhanced_dir}{image_counter - 1:06d}.png"
            try:
                if not os.path.isfile(f"{self.enhanced_dir}{image_counter:06d}.png"):
                    self.image.load(image_counter, self.image_dir)

                    if self.ssim.get(image_counter - 1) == IDENTICAL and os.path.exists(
                        prev_file_path
                    ):
                        shutil.copy(
                            prev_file_path,
                            f"{self.enhanced_dir}{image_counter:06d}.png",
                        )

                    else:
                        self.image.crop(self.gui_values)

                        if enable_enhancement:
                            self.image.colour_enhance(self.gui_values)

                        if white_balance:
                            self.image.white_balance()

                        if self.gui_values.scaling != "None":
                            self.image.picture = self.scale_model.scale_image(
                                self.image.picture
                            )

                        self.image.save(image_counter, self.enhanced_dir)
            except Exception as e:
                self.parent.processing_error.emit(
                    f"Error processing image {image_counter}: {e}"
                )
                return

        self.signals.finished.emit()
