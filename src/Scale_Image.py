import numpy as np
from PyQt6.QtCore import QSize
from typing import Tuple

SIZE_OF_WINDOW_DECORATIONS = 100


class Scale_Image:
    @staticmethod
    def scale_image(image: np.ndarray, screen_size: QSize) -> Tuple[int, int, int, int]:
        # subtract 100 to make whole image fit on screen
        screen_width = screen_size.width() - SIZE_OF_WINDOW_DECORATIONS
        screen_height = screen_size.height() - SIZE_OF_WINDOW_DECORATIONS
        image_height, image_width, _ = image.shape

        scale_factor = min(screen_width / image_width, screen_height / image_height)
        new_width, new_height = int(image_width * scale_factor), int(
            image_height * scale_factor
        )

        top = int((screen_height / 2) - (new_height / 2))
        left = int((screen_width / 2) - (new_width / 2))

        return new_width, new_height, top, left
