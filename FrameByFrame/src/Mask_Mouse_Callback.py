import cv2
import numpy as np
from Blending import Blending
from typing import Tuple

MINIMUM_AFFECTED_AREA = 7
RESET_PREVIOUS_COORDS = -1
MASK_COLOUR = (255, 255, 255)
CLEAR_COLOUR = (0, 0, 0)


class Mask_Mouse_Callback:
    def __init__(self) -> None:
        self.blend_image = Blending()
        self.prevX = RESET_PREVIOUS_COORDS
        self.prevY = RESET_PREVIOUS_COORDS
        self.brush_size = MINIMUM_AFFECTED_AREA
        self.brush_radius = self.brush_size // 2

    def mouse_callback_wrapper(
        self,
        event: int,
        x: int,
        y: int,
        flags: int,
        parameters: Tuple[np.ndarray, np.ndarray, np.ndarray, dict],
    ) -> int:
        editing_image, mask_image, callback_data = parameters

        self.brush_size = callback_data["brush_size"]
        self.brush_radius = self.brush_size // 2

        if x - self.brush_radius < 0:
            x = self.brush_radius

        if y - self.brush_radius < 0:
            y = self.brush_radius

        elif event == cv2.EVENT_RBUTTONDOWN or flags == cv2.EVENT_FLAG_RBUTTON:
            mask_image[
                y - self.brush_radius : y + self.brush_radius,
                x - self.brush_radius : x + self.brush_radius,
            ] = CLEAR_COLOUR

        elif event == cv2.EVENT_LBUTTONDOWN or flags == cv2.EVENT_FLAG_LBUTTON:
            mask_image[
                y : y + self.brush_radius, x : x + self.brush_radius
            ] = MASK_COLOUR

        blended_image = self.blend_image.blend_mask(editing_image, mask_image)
        cv2.imshow("Mask Image", blended_image)

    def reset_coords(self) -> None:
        self.prevX = RESET_PREVIOUS_COORDS
