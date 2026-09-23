import os
import shutil

BACKUP_NUMBER_START = -7
BACKUP_NUMBER_END = -4

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
        except OSError as e:
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
    def find_last_backup(file_path_to_copy_to: str, backup_dir: str) -> str:
        basename = os.path.basename(file_path_to_copy_to)
        filename_without_ext = os.path.splitext(basename)[0]
        prefix = f"{filename_without_ext}_"

        highest_count = 0
        for entry in os.listdir(backup_dir):
            if entry.startswith(prefix):
                count_str = entry[BACKUP_NUMBER_START:BACKUP_NUMBER_END]
                if count_str.isdigit():
                    highest_count = max(highest_count, int(count_str))

        return Backup_Image.get_backup_file_path(
            file_path_to_copy_to, highest_count, backup_dir
        )
