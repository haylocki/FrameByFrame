import os
import queue
import shutil
import time

import psutil
import torch
from PyQt6.QtCore import QObject, QThreadPool, pyqtSignal
from PyQt6.QtWidgets import QMainWindow

from Enhanced_File_Operations import Enhanced_File_Operations
from Gui_Values import Gui_Values
from Image_Processing import Image_Processing_Worker
from Ssim import Ssim

IDENTICAL = 1.0


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
        image_dir: str,
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
        self.completed_threads = 0

        frame_queue: queue.Queue[int] = queue.Queue()
        for image_index in range(1, self.total_images + 1):
            frame_queue.put(image_index)

        has_gpu = torch.cuda.is_available()
        gpu_workers = 1 if has_gpu else 0
        cpu_workers = self.gui_values.threads
        max_threads = gpu_workers + cpu_workers

        devices = ["cuda"] * gpu_workers + ["cpu"] * cpu_workers

        self.thread_pool.setMaxThreadCount(max_threads)
        self.wait_for_free_memory(max_threads)

        self.workers = []
        for device in devices:
            worker = Image_Processing_Worker(
                frame_queue,
                device,
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
            self.workers.append(worker)
            self.thread_pool.start(worker)

    def check_processing_completion(self) -> None:
        self.completed_threads += 1

        if self.completed_threads == self.thread_pool.maxThreadCount():
            self.fill_missing_frames()
            self.thread_pool.clear()
            self.processing_finished.emit()

    def fill_missing_frames(self) -> None:
        """Sequential cleanup pass: copies forward any identical frame that
        was skipped during parallel processing because its predecessor
        wasn't finished yet. Must run strictly in order so cascades of
        consecutive identical frames resolve correctly."""
        for frame_index in range(1, self.total_images + 1):
            current_path = f"{self.enhanced_dir}{frame_index:06d}.png"
            if os.path.isfile(current_path):
                continue

            prev_path = f"{self.enhanced_dir}{frame_index - 1:06d}.png"
            if self.ssim.get(frame_index - 1) == IDENTICAL and os.path.exists(
                prev_path
            ):
                shutil.copy(prev_path, current_path)

    @staticmethod
    def wait_for_free_memory(target_memory_gb: int) -> None:
        while True:
            memory = psutil.virtual_memory()
            free_memory_gb = memory.available / (1024**3)
            if free_memory_gb >= target_memory_gb:
                break

            time.sleep(1)  # Wait for 1 second before checking again
