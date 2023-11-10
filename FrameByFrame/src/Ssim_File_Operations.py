import json
import os


class Ssim_File_Operations:
    def __init__(self):
        self.ssim = []

    def save(self, image_dir: str):
        file_path = f"{image_dir}ssim_values.txt"

        try:
            with open(file_path, "w") as file:
                json.dump(self.ssim, file)
        except OSError as e:
            print(f"Error saving ssim values: {e}")

    def load(self, image_dir: str, total_images: int) -> bool:
        result = False
        file_path = f"{image_dir}ssim_values.txt"

        if os.path.isfile(file_path):
            self.ssim.clear()

            try:
                with open(file_path, "r") as file:
                    loaded_values = json.load(file)
                    self.ssim.extend(loaded_values)
            except FileNotFoundError as e:
                print(f"Error loading ssim values: {e}")

            self.ssim.extend([0] * (total_images - len(self.ssim)))

            result = True
        return result
