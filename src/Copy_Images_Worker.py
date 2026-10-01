from PyQt6.QtCore import QObject, QRunnable, pyqtSignal


class Copy_Images_Worker_Signals(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()


class Copy_Images_Worker(QRunnable):
    def __init__(
        self,
        copy_images,
        image_counter: int,
        image_dir: str,
        backup_dir: str,
        copy_from_image: int,
        copy_to_image: int,
        ssim,
        mask,
    ):
        super().__init__()
        self.signals = Copy_Images_Worker_Signals()
        self.copy_images = copy_images
        self.image_counter = image_counter
        self.image_dir = image_dir
        self.backup_dir = backup_dir
        self.copy_from_image = copy_from_image
        self.copy_to_image = copy_to_image
        self.ssim = ssim
        self.mask = mask

    def run(self) -> None:
        self.copy_images.copy(
            self.image_counter,
            self.image_dir,
            self.backup_dir,
            self.copy_from_image,
            self.copy_to_image,
            self.ssim,
            self.mask,
            progress_callback=self.signals.progress.emit,
        )
        self.signals.finished.emit()
