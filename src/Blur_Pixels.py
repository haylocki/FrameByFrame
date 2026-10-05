import cv2
import numpy as np

from Circular_Brush import Circular_Brush

BLUR_KERNEL_SIZE = 5


class Blur_Pixels:
    @staticmethod
    def blur_adjacent_pixels(
        x: int,
        y: int,
        prev_x: int,
        prev_y: int,
        left_image: np.ndarray,
        neighborhood_radius: int,
    ) -> None:
        Blur_Pixels.blur_region(x, y, left_image, neighborhood_radius)
        Blur_Pixels.blur_region(prev_x, prev_y, left_image, neighborhood_radius)

    @staticmethod
    def blur_region(
        center_x: int,
        center_y: int,
        left_image: np.ndarray,
        neighborhood_radius: int,
    ) -> None:
        height, width = left_image.shape[:2]

        x_start, y_start, x_stop, y_stop = Circular_Brush.get_bounds(
            center_x, center_y, neighborhood_radius, width, height
        )

        if y_start >= y_stop or x_start >= x_stop:
            return

        roi = left_image[y_start:y_stop, x_start:x_stop]
        blurred_roi = cv2.GaussianBlur(roi, (BLUR_KERNEL_SIZE, BLUR_KERNEL_SIZE), 0)

        circular_mask = Circular_Brush.get_mask(
            center_x, center_y, neighborhood_radius, x_start, y_start, x_stop, y_stop
        )

        left_image[y_start:y_stop, x_start:x_stop] = np.where(
            circular_mask[..., None], blurred_roi, roi
        )
