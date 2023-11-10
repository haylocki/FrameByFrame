from Blur_Pixels import Blur_Pixels
from Copy_Pixels import Copy_Pixels
import cv2
import numpy as np
from typing import Tuple

MINIMUM_AFFECTED_AREA = 7
RESET_PREVIOUS_COORDS = -1


class Editor_Mouse_Callback:
    def __init__(self) -> None:
        self.blur_pixels = Blur_Pixels()
        self.copy_pixels = Copy_Pixels()
        self.prevX = RESET_PREVIOUS_COORDS
        self.prevY = RESET_PREVIOUS_COORDS
        self.neighborhood_size = MINIMUM_AFFECTED_AREA
        self.neighborhood_radius = self.neighborhood_size // 2

    def mouse_callback_wrapper(
        self,
        event: int,
        x: int,
        y: int,
        flags: int,
        parameters: Tuple[np.ndarray, np.ndarray, np.ndarray, dict],
    ) -> int:
        editing_image, previous_image, next_image, callback_data = parameters

        self.neighborhood_size = callback_data["neighborhood_size"]
        self.neighborhood_radius = self.neighborhood_size // 2

        if x - self.neighborhood_radius < 0:
            x = self.neighborhood_radius

        if y - self.neighborhood_radius < 0:
            y = self.neighborhood_radius

        if event == cv2.EVENT_MBUTTONDOWN or flags == cv2.EVENT_FLAG_MBUTTON:
            if self.prevX == RESET_PREVIOUS_COORDS:
                self.prevX = x
                self.prevY = y

            self.blur_pixels.blur_adjacent_pixels(
                x,
                y,
                self.prevX,
                self.prevY,
                editing_image,
                self.neighborhood_radius,
                self.neighborhood_size,
            )
            self.prevX, self.prevY = x, y

        elif event == cv2.EVENT_RBUTTONDOWN or flags == cv2.EVENT_FLAG_RBUTTON:
            self.copy_pixels.copy_region(
                x, y, self.neighborhood_radius, editing_image, next_image
            )

        elif event == cv2.EVENT_LBUTTONDOWN or flags == cv2.EVENT_FLAG_LBUTTON:
            self.copy_pixels.copy_region(
                x, y, self.neighborhood_radius, editing_image, previous_image
            )

        cv2.imshow("Edit Image", editing_image)

    def reset_coords(self) -> None:
        self.prevX = RESET_PREVIOUS_COORDS
