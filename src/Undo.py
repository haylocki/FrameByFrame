import shutil
from Backup_Image import Backup_Image

class Undo:
    def __init__(self) -> None:
        self.backup = Backup_Image
        
    def copy(self, image_counter: int, image_dir: str, backup_dir: str):
        file_path_to = f"{image_dir}{image_counter:06d}.png"
        file_path_from = self.backup.find_last_backup(file_path_to, backup_dir)
        shutil.move(file_path_from, file_path_to)
