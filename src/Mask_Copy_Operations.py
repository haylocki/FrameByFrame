import numpy as np

from Backup_Image import Backup_Image
from Blending import Blending
from Image import Image
from Mask import Mask
from Ssim import Ssim


class Mask_Copy_Operations:
    def __init__(self) -> None:
        self.image_1 = Image(None, None)
        self.image_2 = Image(None, None)
        self.backup = Backup_Image
        self.blend = Blending()

    def copy_image(
        self,
        ssim: Ssim,
        image_counter: int,
        mask: Mask,
        image_dir: str,
        delta: int,
    ):
        self.image_1.load(image_counter, image_dir)
        self.image_2.load(image_counter + delta, image_dir)
        self.image_2.picture = Mask_Copy_Operations.masked_copy(
            self.image_1.picture, self.image_2.picture, mask.picture
        )

        self.image_2.save(image_counter + delta, image_dir)
        self.update_ssim(ssim, image_counter)

    def update_ssim(self, ssim: Ssim, image_counter: int) -> None:
        ssim.set(image_counter, 0)
        ssim_value = ssim.calculate(
            image_counter, self.image_1.picture, self.image_2.picture
        )
        ssim.set(image_counter, ssim_value)

    @staticmethod 
    def masked_copy(
        source_image: np.ndarray, destination_image: np.ndarray, mask: np.ndarray
    ) -> np.ndarray:
        return np.where(mask == [0, 0, 0], source_image, destination_image)
