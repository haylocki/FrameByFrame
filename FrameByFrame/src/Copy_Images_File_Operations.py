import os
import shutil
from Ssim import Ssim

IDENTICAL = 1.0


class Copy_Images_File_Operations:
    def copying_backwards(
        self,
        copy_from_image: int,
        copy_to_image: int,
        image_dir: str,
        backup_dir: str,
        ssim: Ssim,
    ):
        file_path_to_copy_from = f"{image_dir}{copy_from_image:06d}.png"
        file_path_to_copy_to = f"{image_dir}{copy_to_image:06d}.png"
        self.backup_image(file_path_to_copy_to, backup_dir)
        self.copy_image(
            file_path_to_copy_from, file_path_to_copy_to, ssim, copy_to_image
        )

    def backup_image(self, file_path_to_copy_from: str, backup_dir: str):
        backup_count = 1
        while os.path.isfile(
            file_path_to_copy_to := self.get_backup_file_path(
                file_path_to_copy_from, backup_count, backup_dir
            )
        ):
            backup_count += 1

        try:
            shutil.copyfile(file_path_to_copy_from, file_path_to_copy_to)
        except IOError as e:
            print(f"Error copying file for backup: {e}")

    @staticmethod
    def copy_image(
        file_path_from: str, file_path_to: str, ssim: Ssim, image_counter: int
    ):
        try:
            shutil.copyfile(file_path_from, file_path_to)
            # ssim = 1.0 means both images are identical
            ssim.set(image_counter, IDENTICAL)
        except IOError as e:
            print(f"Error copying file: {e}")

    @staticmethod
    def get_backup_file_path(
        file_path_to_copy_to: str, count: int, backup_dir: str
    ) -> str:
        basename = os.path.basename(file_path_to_copy_to)
        filename_without_ext = os.path.splitext(basename)[0]
        count_str = f"{count:03d}"

        return f"{backup_dir}{filename_without_ext}_{count_str}.png"

    def find_last_backup(self, file_path_to_copy_to: str, backup_dir: str):
        backup_count = 1

        while True:
            file_path_from = self.get_backup_file_path(
                file_path_to_copy_to, backup_count, backup_dir
            )

            if not os.path.isfile(file_path_from):
                break

            backup_count += 1

        file_path_from = self.get_backup_file_path(
            file_path_to_copy_to, backup_count - 1, backup_dir
        )

        return file_path_from
