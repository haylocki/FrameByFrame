import os
import shutil

BACKUP_NUMBER_START = -7
BACKUP_NUMBER_END = -4


class Backup_Image:
    @staticmethod
    def build_backup_filename(frame_number: int, backup_number: int) -> str:
        return f"{frame_number:06d}_{backup_number:03d}.png"

    @staticmethod
    def create_backup_frame(frame_number: int, image_dir: str, backup_dir: str):
        file_to_backup = f"{image_dir}{frame_number:06d}.png"
        backup_number = 1
        while os.path.isfile(
            file_path_to_copy_to := Backup_Image.get_backup_file_path(
                frame_number, backup_number, backup_dir
            )
        ):
            backup_number += 1

        try:
            shutil.copyfile(file_to_backup, file_path_to_copy_to)
        except OSError as e:
            print(f"Error copying file for backup: {e}")

    @staticmethod
    def get_backup_file_path(
        frame_number: int, backup_number: int, backup_dir: str
    ) -> str:
        filename = Backup_Image.build_backup_filename(frame_number, backup_number)
        return f"{backup_dir}{filename}"

    @staticmethod
    def find_last_backup(frame_number: int, backup_dir: str) -> str:
        prefix = f"{frame_number:06d}_"

        highest_backup_number = 0
        for entry in os.listdir(backup_dir):
            if entry.startswith(prefix):
                current_backup_number = entry[BACKUP_NUMBER_START:BACKUP_NUMBER_END]
                if current_backup_number.isdigit():
                    current_backup_number = int(current_backup_number)
                    highest_backup_number = max(highest_backup_number, current_backup_number)

        return Backup_Image.build_backup_filename(frame_number, highest_backup_number)
