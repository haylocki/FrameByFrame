import numpy as np


class Copy_Pixels:
    @staticmethod
    def copy_region(
        x: int,
        y: int,
        neighborhood_radius: int,
        to_image: np.ndarray,
        from_image: np.ndarray,
    ) -> None:
        height, width = to_image.shape[:2]

        y_start = min(max(y - neighborhood_radius, 0), height)
        y_stop = min(max(y + neighborhood_radius + 1, 0), height)
        x_start = min(max(x - neighborhood_radius, 0), width)
        x_stop = min(max(x + neighborhood_radius + 1, 0), width)

        if y_start >= y_stop or x_start >= x_stop:
            return  # Brush is entirely outside the image — nothing to copy.

        to_image[y_start:y_stop, x_start:x_stop] = from_image[
            y_start:y_stop, x_start:x_stop
        ]
