import os
import queue

import cv2
from PyQt6.QtCore import QObject, QRunnable, pyqtSignal

from Image import Image
from Model_Rrdbnet_Pth import Model_Rrdbnet_Pth
from Model_SRVGGNetCompact_Pth import Model_SRVGGNetCompact_Pth
from Scaling_Model_Factory import Scaling_Model_Factory
from Tile_Benchmark_Coordinator import Tile_Benchmark_Coordinator

IDENTICAL = 1.0
CANDIDATE_TILE_SIZES = (96, 128, 192, 256, 312)


def get_candidate_sizes_for_worker(
    worker_index: int, cpu_worker_count: int
) -> list[int]:
    """Split the candidate tile sizes across however many CPU workers the
    user configured, so benchmarking never uses more cores than requested."""
    return [
        size
        for i, size in enumerate(CANDIDATE_TILE_SIZES)
        if i % cpu_worker_count == worker_index
    ]


class Image_Processing_Worker_Signals(QObject):
    finished = pyqtSignal()


class Image_Processing_Worker(QRunnable):
    def __init__(
        self,
        frame_queue,
        device,
        enhanced_dir,
        gui_values,
        scene_parameters,
        ssim,
        image_dir,
        current_dir,
        total_images,
        parent=None,
        progress_callback=None,
        worker_index: int | None = None,
        cpu_worker_count: int = 0,
        tile_benchmark_coordinator: Tile_Benchmark_Coordinator | None = None,
    ):
        super().__init__()
        self.signals = Image_Processing_Worker_Signals()
        self.frame_queue = frame_queue
        self.device = device
        self.gui_values = gui_values
        self.scene_parameters = scene_parameters
        self.current_dir = current_dir
        self.image_dir = image_dir
        self.enhanced_dir = enhanced_dir
        self.ssim = ssim
        self.total_images = total_images
        self.parent = parent
        self.progress_callback = progress_callback
        self.worker_index = worker_index
        self.cpu_worker_count = cpu_worker_count
        self.tile_benchmark_coordinator = tile_benchmark_coordinator
        self.scale_model = None

    def process_frame(self, frame_index: int) -> bool:
        assert self.progress_callback is not None
        assert self.parent is not None

        scene_gui_values = self.scene_parameters.for_frame(frame_index)
        white_balance = scene_gui_values.white_balance
        enable_enhancement = scene_gui_values.enable_enhancement

        frames_remaining = self.frame_queue.qsize()
        frames_attempted = self.total_images - frames_remaining
        progress_percentage = (frames_attempted * 50) // self.total_images
        self.progress_callback.emit(progress_percentage)

        same_scene_as_previous = self.scene_parameters.for_frame(
            frame_index
        ) is self.scene_parameters.for_frame(frame_index - 1)

        try:
            if not os.path.isfile(
                f"{self.enhanced_dir}{frame_index:06d}.png"
            ) and not (
                self.ssim.get(frame_index - 1) == IDENTICAL and same_scene_as_previous
            ):
                self.image.load(frame_index, self.image_dir)
                self.image.crop(scene_gui_values)

                if enable_enhancement:
                    self.image.colour_enhance(scene_gui_values)

                if white_balance:
                    self.image.white_balance()

                if self.gui_values.scaling != "None":
                    assert self.scale_model is not None
                    self.image.picture = self.scale_model.scale_image(
                        self.image.picture
                    )

                self.image.save(frame_index, self.enhanced_dir)
        except Exception as e:  # noqa: BLE001
            self.parent.processing_error.emit(
                f"Error processing image {frame_index}: {e}"
            )
            return False

        return True

    def run(self):

        assert self.progress_callback is not None
        assert self.parent is not None

        # TensorFlow models
        self.image = Image(None, None)

        if self.gui_values.scaling != "None":
            self.scale_model, _ = Scaling_Model_Factory.load_model(
                self.gui_values.scaling, self.current_dir, self.device
            )

            if isinstance(
                self.scale_model, (Model_Rrdbnet_Pth, Model_SRVGGNetCompact_Pth)
            ):
                self.benchmark_tile_size()

        while True:
            try:
                frame_index = self.frame_queue.get_nowait()
            except queue.Empty:
                break

            if not self.process_frame(frame_index):
                return

        self.signals.finished.emit()

    def benchmark_tile_size(self) -> None:
        assert self.scale_model is not None
        sample_image = cv2.imread(f"{self.image_dir}000001.png")

        if sample_image is None:
            return

        if self.device == "cuda":
            self.scale_model.find_fastest_tile_size(sample_image)
            return

        if self.tile_benchmark_coordinator is None:
            return

        assert self.worker_index is not None

        candidate_sizes = get_candidate_sizes_for_worker(
            self.worker_index, self.cpu_worker_count
        )

        for size in candidate_sizes:
            elapsed = self.scale_model.time_tile_size(sample_image, size)

            if elapsed is not None:
                self.tile_benchmark_coordinator.report(size, elapsed)

        winning_size = self.tile_benchmark_coordinator.wait_and_get_winner()
        self.scale_model.working_tile_size = winning_size

        if self.worker_index == 0:
            print(f"Selected fastest CPU tile size: {winning_size}")
