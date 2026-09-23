import os
import shutil

BACKUP_NUMBER_START = -7
BACKUP_NUMBER_END = -4


class Backup_Image:
    @staticmethod
    def build_backup_filename(frame_number: int, count: int) -> str:
        return f"{frame_number:06d}_{count:03d}.png"
    
    @staticmethod
    def create_backup_frame(frame_number: int, image_dir: str, backup_dir: str):
        file_to_backup = f"{image_dir}{frame_number:06d}.png"
        backup_count = 1
        while os.path.isfile(
            file_path_to_copy_to := Backup_Image.get_backup_file_path(
                frame_number, backup_count, backup_dir
            )
        ):
            backup_count += 1

        try:
            shutil.copyfile(file_to_backup, file_path_to_copy_to)
        except OSError as e:
            print(f"Error copying file for backup: {e}")

    @staticmethod
    def get_backup_file_path(
        image_counter: int, count: int, backup_dir: str
    ) -> str:
        filename = Backup_Image.build_backup_filename(image_counter, count)
        return f"{backup_dir}{filename}"

    @staticmethod
    def find_last_backup(frame_number: int, backup_dir: str) -> str:
        prefix = f"{frame_number:06d}_"

        highest_count = 0
        for entry in os.listdir(backup_dir):
            if entry.startswith(prefix):
                count_str = entry[BACKUP_NUMBER_START:BACKUP_NUMBER_END]
                if count_str.isdigit():
                    highest_count = max(highest_count, int(count_str))

        return Backup_Image.build_backup_filename(frame_number, highest_count)
            
