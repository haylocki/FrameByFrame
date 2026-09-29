import cv2
import numpy as np

from Blending import Blending
from Circular_Brush import Circular_Brush

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
        parameters: tuple[np.ndarray, np.ndarray, dict] | None,
    ) -> None:

        if parameters is None:
            return

        editing_image, mask_image, callback_data = parameters

        self.brush_size = callback_data["brush_size"]
        self.brush_radius = self.brush_size // 2

        height, width = mask_image.shape[:2]

        x_start, y_start, x_stop, y_stop = Circular_Brush.get_bounds(
            x, y, self.brush_radius, width, height
        )

        if y_start >= y_stop or x_start >= x_stop:
            return

        circular_mask = Circular_Brush.get_mask(
            x,
            y,
            self.brush_radius,
            x_start,
            y_start,
            x_stop,
            y_stop,
        )

        if event == cv2.EVENT_RBUTTONDOWN or flags == cv2.EVENT_FLAG_RBUTTON:
            mask_image[y_start:y_stop, x_start:x_stop][circular_mask] = CLEAR_COLOUR

        elif event == cv2.EVENT_LBUTTONDOWN or flags == cv2.EVENT_FLAG_LBUTTON:
            mask_image[y_start:y_stop, x_start:x_stop][circular_mask] = MASK_COLOUR

        blended_image = self.blend_image.blend_mask(editing_image, mask_image)
        cv2.imshow("Mask Image", blended_image)

    def reset_coords(self) -> None:
        self.prevX = RESET_PREVIOUS_COORDS
        self.prevY = RESET_PREVIOUS_COORDS
