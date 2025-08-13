import numpy as np
from skimage.metrics import structural_similarity as calc_ssim
from Ssim_File_Operations import Ssim_File_Operations


class Ssim(Ssim_File_Operations):
    def get(self, index: int) -> float:
        return self.ssim[index]

    def set(self, index, value):
        self.ssim[index] = value

    def calculate(self, index: int, image1: np.ndarray, image2: np.ndarray) -> float:
        current_ssim = self.ssim[index]
        if current_ssim == None:
            current_ssim = calc_ssim(image1, image2, channel_axis=2)
            current_ssim = round(current_ssim, 4)
        return current_ssim

    def clear_values(self, total_images: int):
        self.ssim.clear()
        self.ssim.extend([None] * (total_images + 1))
