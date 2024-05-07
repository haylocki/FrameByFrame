import cv2
from Editor_Mouse_Callback import Editor_Mouse_Callback
import numpy as np
from PyQt6.QtCore import QSize
from Scale_Image import Scale_Image

EQUALS = 61
MINUS = 45
PLUS = 43
RADIUS_SIZE_ADJUST = 2
MINIMUM_AFFECTED_AREA = 7


class Scratch_Remover:
    def __init__(self):
        self.si = Scale_Image()
        self.neighborhood_size = MINIMUM_AFFECTED_AREA
        self.callback_data = {
            "neighborhood_size": self.neighborhood_size,
        }

    def edit_image(
        self,
        editing_image: np.ndarray,
        previous_image: np.ndarray,
        next_image: np.ndarray,
        screen_size: QSize,
    ) -> bool:
        scaled_width, scaled_height, top, left = self.si.scale_image(
            editing_image, screen_size
        )

        cv2.namedWindow("Edit Image", cv2.WINDOW_GUI_NORMAL)
        cv2.resizeWindow("Edit Image", scaled_width, scaled_height)
        cv2.moveWindow("Edit Image", left, top)
        cv2.imshow("Edit Image", editing_image)

        mouse_callback_handler = Editor_Mouse_Callback()

        cv2.setMouseCallback(
            "Edit Image",
            mouse_callback_handler.mouse_callback_wrapper,
            (editing_image, previous_image, next_image, self.callback_data),
        )

        while True:
            key = cv2.waitKey(1) & 0x_FF

            if key != 255:
                if chr(key).upper() == "S":
                    mouse_callback_handler.reset_coords()
                    save = True
                    break

                elif chr(key).upper() == "X":
                    mouse_callback_handler.reset_coords()
                    save = False
                    break

                elif key == PLUS or key == EQUALS:
                    self.adjust_radius_size(RADIUS_SIZE_ADJUST)

                elif key == MINUS:
                    self.adjust_radius_size(-RADIUS_SIZE_ADJUST)

        cv2.destroyAllWindows()
        return save

    def adjust_radius_size(self, delta: int) -> None:
        self.neighborhood_size += delta

        if self.neighborhood_size < MINIMUM_AFFECTED_AREA:
            self.neighborhood_size = MINIMUM_AFFECTED_AREA

        self.callback_data["neighborhood_size"] = self.neighborhood_size
