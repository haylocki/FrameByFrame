import json
import os
from bisect import bisect_right

from Gui_Values import Gui_Values
from Scene import Scene

SCENE_FIELDS = [
    "alpha",
    "beta",
    "compress",
    "theta",
    "phi",
    "enable_enhancement",
    "white_balance",
]


class Scene_Parameters:
    def __init__(self, scenes: list[Scene]):
        self.scenes = sorted(scenes, key=lambda scene: scene.start_frame)
        self.start_frames = [scene.start_frame for scene in self.scenes]

    def for_frame(self, frame_index: int) -> Gui_Values:
        if not self.scenes:
            return Gui_Values()

        position = bisect_right(self.start_frames, frame_index) - 1
        position = max(position, 0)
        return self.scenes[position].gui_values

    def has_scene_at(self, frame_index: int) -> bool:
        return frame_index in self.start_frames

    def add_scene(self, frame_index: int, gui_values: Gui_Values) -> None:
        self.remove_scene(frame_index)  # replace if one already exists here
        self.scenes.append(Scene(frame_index, gui_values))
        self.scenes.sort(key=lambda scene: scene.start_frame)
        self.start_frames = [scene.start_frame for scene in self.scenes]

    def remove_scene(self, frame_index: int) -> None:
        self.scenes = [s for s in self.scenes if s.start_frame != frame_index]
        self.start_frames = [scene.start_frame for scene in self.scenes]

    def save(self, image_dir: str) -> None:
        file_path = os.path.join(image_dir, "scenes.txt")
        data = {
            scene.start_frame: {
                field: getattr(scene.gui_values, field) for field in SCENE_FIELDS
            }
            for scene in self.scenes
        }

        try:
            with open(file_path, "w") as file:
                json.dump(data, file)
        except OSError as e:
            print(f"Error saving scenes: {e}")

    @staticmethod
    def _ensure_file_exists(file_path: str) -> bool:
        """Create the scenes file containing an empty JSON object if it doesn't exist.

        Returns True if the file exists (or was created), False if creation failed.
        """
        if os.path.exists(file_path):
            return True

        try:
            with open(file_path, "w") as file:
                file.write("{}")
            return True
        except OSError as e:
            print(f"Error creating scenes file: {e}")
            return False

    @staticmethod
    def _parse_scenes(data: dict) -> list:
        scenes = []
        for start_frame_str, values in data.items():
            gui_values = Gui_Values()
            for field, value in values.items():
                setattr(gui_values, field, value)
            scenes.append(Scene(int(start_frame_str), gui_values))
        return scenes

    @classmethod
    def load(cls, image_dir: str) -> "Scene_Parameters":
        file_path = os.path.join(image_dir, "scenes.txt")

        if not cls._ensure_file_exists(file_path):
            return cls([])

        try:
            with open(file_path) as file:
                data = json.load(file)
                scenes = cls._parse_scenes(data)
        except (OSError, json.JSONDecodeError, ValueError) as e:
            print(f"Error loading scenes: {e}")
            return cls([])

        return cls(scenes)
