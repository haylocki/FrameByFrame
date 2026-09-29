import numpy as np

from Circular_Brush import Circular_Brush


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

        x_start, y_start, x_stop, y_stop = Circular_Brush.get_bounds(
            x, y, neighborhood_radius, width, height
        )

        if y_start >= y_stop or x_start >= x_stop:
            return

        circular_mask = Circular_Brush.get_mask(
            x,
            y,
            neighborhood_radius,
            x_start,
            y_start,
            x_stop,
            y_stop,
        )

        to_roi = to_image[y_start:y_stop, x_start:x_stop]
        from_roi = from_image[y_start:y_stop, x_start:x_stop]

        to_roi[:] = np.where(
            circular_mask[..., None],
            from_roi,
            to_roi,
        )
