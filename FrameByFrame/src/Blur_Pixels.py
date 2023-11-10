import cv2
import numpy as np


class Blur_Pixels:
    def blur_adjacent_pixels(
        self,
        x: int,
        y: int,
        prevX: int,
        prevY: int,
        left_image: np.ndarray,
        neighborhood_radius: int,
        neighborhood_size: int,
    ) -> None:
        # Get the region of interest around the current and previous pixel
        curr_roi = left_image[
            y - neighborhood_radius : y + neighborhood_radius + 1,
            x - neighborhood_radius : x + neighborhood_radius + 1,
        ]
        prev_roi = left_image[
            prevY - neighborhood_radius : prevY + neighborhood_radius + 1,
            prevX - neighborhood_radius : prevX + neighborhood_radius + 1,
        ]

        # Blur the region of interest
        blurred_curr_roi = cv2.blur(curr_roi, (neighborhood_size, neighborhood_size))
        blurred_prev_roi = cv2.blur(prev_roi, (neighborhood_size, neighborhood_size))

        # Update the image with the blurred regions
        left_image[
            y - neighborhood_radius : y + neighborhood_radius + 1,
            x - neighborhood_radius : x + neighborhood_radius + 1,
        ] = blurred_curr_roi
        left_image[
            prevY - neighborhood_radius : prevY + neighborhood_radius + 1,
            prevX - neighborhood_radius : prevX + neighborhood_radius + 1,
        ] = blurred_prev_roi
