from Backup_Image import Backup_Image
from Blending import Blending
from Image import Image
from Mask import Mask
from Ssim import Ssim

IDENTICAL = 1.0


class Copy_Images_File_Operations:
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
        try:
            self.image_1.load(image_counter, image_dir)
            self.image_2.load(image_counter + delta, image_dir)
            self.image_2.picture = self.blend.blend_images(
                self.image_1.picture, self.image_2.picture, mask.picture
            )

            self.image_2.save(image_counter + delta, image_dir)
            ssim.set(image_counter, 0)
            ssim.calculate(image_counter, self.image_1.picture, self.image_2.picture)
        except IOError as e:
            print(f"Error copying file: {e}")
