import cv2
from Blending import Blending
from Brush_Radius import Brush_Radius
from Mask_Mouse_Callback import Mask_Mouse_Callback
import numpy as np
from PyQt6.QtCore import QSize
from Scale_Image import Scale_Image

EQUALS = 61
MINUS = 45
PLUS = 43
RADIUS_DELTA = 2
MINIMUM_BRUSH_SIZE = 2


class Mask:
    def __init__(self):
        self.si = Scale_Image()
        self.blend = Blending()
        self.brush_radius = Brush_Radius()
        self.blended_image = None
        self.picture = None
        self.brush_size = 20
        self.callback_data = {
            "brush_size": self.brush_size,
        }

    def create(self, height: int, width: int):
        self.picture = np.zeros((height, width, 3), dtype=np.uint8)

    def edit(
        self,
        editing_image: np.ndarray,
        screen_size: QSize,
    ) -> bool:
        self.blended_image = self.blend.blend_mask(editing_image, self.picture)
        scaled_width, scaled_height, top, left = self.si.scale_image(
            editing_image, screen_size
        )

        cv2.namedWindow("Mask Image", cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow("Mask Image", scaled_width, scaled_height)
        cv2.moveWindow("Mask Image", left, top)
        cv2.imshow("Mask Image", self.blended_image)

        mouse_callback_handler = Mask_Mouse_Callback()

        cv2.setMouseCallback(
            "Mask Image",
            mouse_callback_handler.mouse_callback_wrapper,
            (editing_image, self.picture, self.callback_data),
        )

        while True:
            key = cv2.waitKey(1) & 0x_FF

            if key != 255:
                if chr(key).upper() == "S":
                    mouse_callback_handler.reset_coords()
                    break

                elif chr(key).upper() == "X":
                    mouse_callback_handler.reset_coords()
                    self.picture[:] = 0
                    break

                elif key == PLUS or key == EQUALS:
                    self.brush_size = self.brush_radius.adjust(
                        self.brush_size, RADIUS_DELTA, MINIMUM_BRUSH_SIZE
                    )
                    self.callback_data["brush_size"] = self.brush_size

                elif key == MINUS:
                    self.brush_size = self.brush_radius.adjust(
                        self.brush_size, -RADIUS_DELTA, MINIMUM_BRUSH_SIZE
                    )
                    self.callback_data["brush_size"] = self.brush_size

        cv2.destroyAllWindows()
