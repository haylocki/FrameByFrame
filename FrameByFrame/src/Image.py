import cv2
import numpy as np
from Gui_Values import Gui_Values
from PyQt6.QtGui import QImage, QPixmap

MINIMUM_IMAGE_SIZE = 14


class Image:
    def __init__(self, image_frame, image_label):
        self.picture_frame = image_frame
        self.picture_label = image_label
        self.picture = np.zeros(
            (MINIMUM_IMAGE_SIZE, MINIMUM_IMAGE_SIZE, 3), dtype=np.uint8
        )

    def load(self, image_counter: int, image_dir: str):
        try:
            self.picture = cv2.imread(f"{image_dir}{image_counter:06d}.png")
        except cv2.error as e:
            print(f"Error loading image {image_counter}: {e}")

    def save(self, image_counter: int, image_dir: str):
        try:
            cv2.imwrite(f"{image_dir}{image_counter:06d}.png", self.picture)
        except cv2.error as e:
            print(f"Error saving image {image_counter}: {e}")

    def display(self):
        qimage = self.convert_cv2_to_qimage(self.picture)
        pixmap_image = QPixmap.fromImage(qimage)
        self.picture_frame.setPixmap(pixmap_image)

    def display_image_number(self, image_counter: int):
        self.picture_label.setText("{:06d}".format(image_counter))

    def white_balance(self):
        img_LAB = cv2.cvtColor(self.picture, cv2.COLOR_BGR2LAB)

        # Calculate the average 'a' and 'b' values within a region of interest (ROI)
        roi = img_LAB[:, :, 0] / 255.0  # Use the 'L' channel as the mask

        # Ensure that there are no zero weights to prevent division by zero
        if np.sum(roi) > 0:
            avg_a = np.average(img_LAB[:, :, 1], weights=roi)
            avg_b = np.average(img_LAB[:, :, 2], weights=roi)

            # Apply white balancing using dynamically calculated scaling factors
            img_LAB[:, :, 1] = img_LAB[:, :, 1] - ((avg_a - 128) * roi * 1.2)
            img_LAB[:, :, 2] = img_LAB[:, :, 2] - ((avg_b - 128) * roi * 1.2)

            # Clip 'a' and 'b' values to the valid range
            img_LAB[:, :, 1] = np.clip(img_LAB[:, :, 1], 0, 255)
            img_LAB[:, :, 2] = np.clip(img_LAB[:, :, 2], 0, 255)

            self.picture = cv2.cvtColor(img_LAB, cv2.COLOR_LAB2BGR)
        else:
            # Handle the case where all weights are zero (avoid division by zero)
            pass

    def crop(self, gui_values: Gui_Values):
        top = gui_values.crop_top
        bottom = gui_values.crop_bottom
        left = gui_values.crop_left
        right = gui_values.crop_right

        new_height = self.picture.shape[0] - top - bottom
        new_width = self.picture.shape[1] - left - right
        # Ensure even dimensions
        new_height += new_height % 2
        new_width += new_width % 2

        self.picture = self.picture[
            top : top + new_height - 1, left : left + new_width - 1
        ]
        self.picture = cv2.resize(self.picture, (new_width, new_height))

    # The following method is modified from code by samkhan13 here:
    # https://stackoverflow.com/questions/19363293/whats-the-fastest-way-to-increase-color-image-contrast-with-opencv-in-python-c/19384041#19384041
    def colour_enhance(self, gui_values: Gui_Values):
        max_intensity = 255.0  # depends on dtype of image data
        self.picture = (max_intensity / gui_values.phi) * (
            self.picture / (max_intensity / gui_values.theta)
        ) ** gui_values.compress

        self.picture = np.int16(self.picture)
        self.picture = (
            self.picture * (gui_values.alpha / 127 + 1)
            - gui_values.alpha
            + gui_values.beta
        )
        self.picture = np.clip(self.picture, 0, 255)
        self.picture = np.uint8(self.picture)

    @staticmethod
    def convert_cv2_to_qimage(cv2Image: np.ndarray):
        height, width, channel = cv2Image.shape
        bytes_per_line = channel * width
        qImage = QImage(
            cv2Image.data, width, height, bytes_per_line, QImage.Format.Format_BGR888
        )
        return qImage
