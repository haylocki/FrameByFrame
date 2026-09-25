import cv2
import numpy as np


class Blending:
    def blend_mask(
        self, editing_image: np.ndarray, mask_image: np.ndarray
    ) -> np.ndarray:
        alpha = 0.5
        blended_image = cv2.addWeighted(editing_image, 1 - alpha, mask_image, alpha, 0)

        return blended_image
