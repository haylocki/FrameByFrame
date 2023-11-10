import shutil
from Copy_Images_File_Operations import Copy_Images_File_Operations
from Ssim import Ssim


class Copy_Images(Copy_Images_File_Operations):
    def copy_images(
        self,
        image_counter: int,
        image_dir: str,
        backup_dir: str,
        copy_from_image: int,
        copy_to_image: int,
        ssim: Ssim,
    ):
        if copy_from_image == 0:  # only copying one frame
            copy_from_image = image_counter
            copy_to_image = image_counter + 1

        if copy_from_image > copy_to_image:
            self.copying_backwards(
                copy_from_image, copy_to_image, image_dir, backup_dir, ssim
            )
            copy_from_image, copy_to_image = copy_to_image, copy_from_image

        for image_counter in range(copy_from_image, copy_to_image):
            file_path_to_copy_from = f"{image_dir}{image_counter:06d}.png"
            file_path_to_copy_to = f"{image_dir}{image_counter + 1:06d}.png"
            self.backup_image(file_path_to_copy_to, backup_dir)
            self.copy_image(
                file_path_to_copy_from, file_path_to_copy_to, ssim, image_counter
            )

    def undo(self, image_counter: int, image_dir: str, backup_dir: str):
        count = 1
        file_path_to = f"{image_dir}{image_counter:06d}.png"
        file_path_from = self.find_last_backup(file_path_to, backup_dir)
        shutil.move(file_path_from, file_path_to)
