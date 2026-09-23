import cv2
import numpy as np


class Blur_Pixels:
    @staticmethod
    def blur_adjacent_pixels(
        x: int,
        y: int,
        prev_x: int,
        prev_y: int,
        left_image: np.ndarray,
        neighborhood_radius: int,
        neighborhood_size: int,
    ) -> None:
        Blur_Pixels.blur_region(x, y, left_image, neighborhood_radius, neighborhood_size)
        Blur_Pixels.blur_region(
            prev_x, prev_y, left_image, neighborhood_radius, neighborhood_size
        )

    @staticmethod
    def blur_region(
        center_x: int,
        center_y: int,
        left_image: np.ndarray,
        neighborhood_radius: int,
        neighborhood_size: int,
    ) -> None:
        height, width = left_image.shape[:2]

        y_start = min(max(center_y - neighborhood_radius, 0), height)
        y_stop = min(max(center_y + neighborhood_radius + 1, 0), height)
        x_start = min(max(center_x - neighborhood_radius, 0), width)
        x_stop = min(max(center_x + neighborhood_radius + 1, 0), width)

        if y_start >= y_stop or x_start >= x_stop:
            return  # Brush is entirely outside the image — nothing to draw.

        roi = left_image[y_start:y_stop, x_start:x_stop]
        blurred_roi = cv2.blur(roi, (neighborhood_size, neighborhood_size))

        circular_mask = Blur_Pixels.get_circular_mask(
            center_x, center_y, neighborhood_radius, x_start, y_start, x_stop, y_stop
        )

        left_image[y_start:y_stop, x_start:x_stop] = np.where(
            circular_mask[..., None], blurred_roi, roi
        )
        
    @staticmethod
    def get_circular_mask(
        center_x: int,
        center_y: int,
        radius: int,
        x_start: int,
        y_start: int,
        x_stop: int,
        y_stop: int,
    ) -> np.ndarray:
        actual_y = np.arange(y_start, y_stop)[:, None]
        actual_x = np.arange(x_start, x_stop)[None, :]

        distance_squared = (actual_x - center_x) ** 2 + (actual_y - center_y) ** 2
        return distance_squared <= radius**2
