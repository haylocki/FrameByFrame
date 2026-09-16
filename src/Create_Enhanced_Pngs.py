import numpy as np
import psutil
import time
from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import QMainWindow
from Enhanced_File_Operations import Enhanced_File_Operations
from Gui_Values import Gui_Values
from Image_Processing import Image_Processing_Worker
from Ssim import Ssim

class Enhanced_Png_Creator(QObject):
    processing_finished = pyqtSignal()
    processing_error = pyqtSignal(str)
    progress_callback = pyqtSignal(int)

    def __init__(self, update_progress_callback):
        super().__init__()
        self.progress_callback.connect(update_progress_callback)
        self.thread_pool = QThreadPool()

    def create_enhanced_pngs(
        self,
        gui_values: Gui_Values,
        image_dir: np.ndarray,
        current_dir: str,
        total_images: int,
        ssim: Ssim,
        window: QMainWindow,
    ) -> None:
        self.gui_values = gui_values
        self.ssim = ssim
        self.image_dir = image_dir
        self.current_dir = current_dir
        self.total_images = total_images
        self.previous_progress = 0
        self.thread_pool.setMaxThreadCount(gui_values.threads)
        self.enhanced_dir = f"{image_dir}enhanced/"
        self.enhanced_directory = Enhanced_File_Operations(self.enhanced_dir)
        self.enhanced_directory.remove(window)
        self.enhanced_directory.create()
        self.process_images()

    def process_images(self) -> None:
        max_threads = self.gui_values.threads
        images_per_thread = self.total_images // max_threads
        remaining_images = self.total_images % max_threads
        self.completed_threads = 0

        for thread_idx in range(max_threads):
            # Make sure we have enough memory free to use scaling model
            self.wait_for_free_memory(1)
            start_image_index = thread_idx * images_per_thread + 1
            end_image_index = start_image_index + images_per_thread

            if end_image_index + remaining_images >= self.total_images:
                end_image_index = self.total_images + 1

            worker = Image_Processing_Worker(
                start_image_index,
                end_image_index,
                self.enhanced_dir,
                self.gui_values,
                self.ssim,
                self.image_dir,
                self.current_dir,
                self.total_images,
                self,
                self.progress_callback,
            )
            worker.signals.finished.connect(self.check_processing_completion)
            self.thread_pool.start(worker)

    def check_processing_completion(self) -> None:
        self.completed_threads += 1

        if self.completed_threads == self.thread_pool.maxThreadCount():
            self.thread_pool.clear()
            self.processing_finished.emit()

    @staticmethod
    def wait_for_free_memory(target_memory_gb: int) -> None:
        while True:
            memory = psutil.virtual_memory()
            free_memory_gb = memory.available / (1024**3)
            if free_memory_gb >= target_memory_gb:
                break

            time.sleep(1)  # Wait for 1 second before checking again
