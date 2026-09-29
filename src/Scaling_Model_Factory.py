from typing import Any

from Configurable_Scaling_Model import Configurable_Scaling_Model
from Model_Pb import Model_Pb
from Model_Rrdbnet_Pth import Model_Rrdbnet_Pth
from Model_SRVGGNetCompact_Pth import Model_SRVGGNetCompact_Pth

MULTIPLE_SCALES = False
SINGLE_SCALE = True


class Scaling_Model_Factory:
    """Create the appropriate image scaling model for a scaling method."""

    @staticmethod
    def load_model(
        scaling: str,
        current_dir: str,
        device: str,
    ) -> tuple[Any, bool]:
        """Create and configure the scaling model.

        Args:
            scaling: Scaling method selected by the GUI.
            current_dir: Directory containing the scaling models.
            device: Device on which the model should run.

        Returns:
            A tuple containing the scaling model and its single-scale mode.
        """
        if scaling.startswith(("fsrc", "edsr")):
            model = Model_Pb()
            model.set_scaling_model(scaling, current_dir, device)
            return model, SINGLE_SCALE

        if scaling.startswith(("RealAnimeV3", "rybu")):
            model = Model_SRVGGNetCompact_Pth()
            is_single_scale = SINGLE_SCALE

        elif scaling.startswith("RealESRGAN"):
            model = Model_Rrdbnet_Pth()
            is_single_scale = MULTIPLE_SCALES

        elif scaling.startswith(("RealAnime6B", "UltraSharp")):
            model = Model_Rrdbnet_Pth()
            is_single_scale = SINGLE_SCALE

        else:
            raise ValueError(f"Unknown scaling method: {scaling}")

        Scaling_Model_Factory.setup_model(
            model,
            is_single_scale,
            scaling,
            current_dir,
            device,
        )

        return model, is_single_scale

    @staticmethod
    def setup_model(
        model: Configurable_Scaling_Model,
        single_scale: bool,
        scaling: str,
        current_dir: str,
        device: str,
    ) -> None:
        """Configure and create a PyTorch scaling model.

        Args:
            model: PyTorch scaling model instance to configure.
            single_scale: Whether the model operates at a single scale.
            scaling: Selected scaling model name.
            current_dir: Current application directory.
            device: Device on which the model should run.

        Returns:
            None.
        """
        model.set_single_scale(single_scale)
        model.set_scaling_model(scaling, current_dir, device)
        model.create_model()
