import numpy as np


class Circular_Brush:
    @staticmethod
    def get_bounds(
        center_x: int,
        center_y: int,
        radius: int,
        width: int,
        height: int,
    ) -> tuple[int, int, int, int]:
        x_start = max(center_x - radius, 0)
        x_stop = min(center_x + radius + 1, width)
        y_start = max(center_y - radius, 0)
        y_stop = min(center_y + radius + 1, height)

        return x_start, y_start, x_stop, y_stop

    @staticmethod
    def get_mask(
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

        distance_squared = (
            (actual_x - center_x) ** 2
            + (actual_y - center_y) ** 2
        )

        return distance_squared <= radius**2
