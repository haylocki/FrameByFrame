import torch
from Model_Pth import Model_Pth
from utils.architecture.RRDB import RRDBNet


class Model_Rrdbnet_Pth(Model_Pth):
    def create_model(self):
        state_dict = torch.load(
            self.model_file_path, map_location=torch.device(self.device)
        )
        self.model = RRDBNet(state_dict)
        self.model = self.model.to(self.device)
        self.model.eval()
