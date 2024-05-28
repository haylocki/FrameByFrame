import numpy as np


class Copy_Pixels:
    def copy_region(
        self,
        x: int,
        y: int,
        neighborhood_radius: int,
        to_image: np.ndarray,
        from_image: np.ndarray,
    ) -> None:
        roi_y_start = y - neighborhood_radius
        roi_y_end = y + neighborhood_radius + 1
        roi_x_start = x - neighborhood_radius
        roi_x_end = x + neighborhood_radius + 1

        to_image[roi_y_start:roi_y_end, roi_x_start:roi_x_end] = from_image[
            roi_y_start:roi_y_end, roi_x_start:roi_x_end
        ]
