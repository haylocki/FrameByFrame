import os
import shutil


class Backup_Image:
    @staticmethod
    def image(image_counter: int, image_dir: str, backup_dir: str):
        file_to_backup = f"{image_dir}{image_counter:06d}.png"
        backup_count = 1
        while os.path.isfile(
            file_path_to_copy_to := Backup_Image.get_backup_file_path(
                file_to_backup, backup_count, backup_dir
            )
        ):
            backup_count += 1

        try:
            shutil.copyfile(file_to_backup, file_path_to_copy_to)
        except IOError as e:
            print(f"Error copying file for backup: {e}")

    @staticmethod
    def get_backup_file_path(
        file_path_to_copy_to: str, count: int, backup_dir: str
    ) -> str:
        basename = os.path.basename(file_path_to_copy_to)
        filename_without_ext = os.path.splitext(basename)[0]
        count_str = f"{count:03d}"

        return f"{backup_dir}{filename_without_ext}_{count_str}.png"

    @staticmethod
    def find_last_backup(file_path_to_copy_to: str, backup_dir: str):
        backup_count = 1

        while True:
            file_path_from = Backup_Image.get_backup_file_path(
                file_path_to_copy_to, backup_count, backup_dir
            )

            if not os.path.isfile(file_path_from):
                break

            backup_count += 1

        file_path_from = Backup_Image.get_backup_file_path(
            file_path_to_copy_to, backup_count - 1, backup_dir
        )

        return file_path_from
