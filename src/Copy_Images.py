from Copy_Images_File_Operations import Copy_Images_File_Operations
from Mask import Mask
from Ssim import Ssim

FORWARD = 1
BACKWARDS = -1


class Copy_Images(Copy_Images_File_Operations):
    def custom_range(self, start, end):
        step = 1 if start <= end else -1
        current = start
        while (current < end and step > 0) or (current > end and step < 0):
            yield current
            current += step

    def copy(
        self,
        image_counter: int,
        image_dir: str,
        backup_dir: str,
        copy_from_image: int,
        copy_to_image: int,
        ssim: Ssim,
        mask: Mask,
    ):
        delta = FORWARD
        if copy_from_image == 0:  # only copying one frame
            copy_from_image = image_counter
            copy_to_image = image_counter + 1

        if copy_from_image > copy_to_image:
            delta = BACKWARDS

        for image_counter in self.custom_range(copy_from_image, copy_to_image):
            self.backup.image(image_counter + delta, image_dir, backup_dir)
            self.copy_image(
                ssim,
                image_counter,
                mask,
                image_dir,
                delta,
            )
