import cv2
import os
import numpy as np
import torch


class Model_Pb:
    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.scaling = None
        self.model_file_path = None
        self.model = cv2.dnn_superres.DnnSuperResImpl_create()

    def scale_image(self, image: np.ndarray) -> np.ndarray:
        image = self.model.upsample(image)

        return image

    def set_scaling_model(self, scaling: str, current_dir: str):
        self.model_file_path = f"{current_dir}/src/models/{scaling}.pb"
        self.model.readModel(self.model_file_path)
        self.model.setModel(scaling[:-2], int(scaling[-1]))

        if torch.cuda.is_available():
            self.model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
