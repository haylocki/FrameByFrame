from typing import Protocol


class ConfigurableScalingModel(Protocol):
    """Interface required by the scaling model factory."""

    def set_single_scale(self, is_single_scale: bool) -> None:
        """Set whether the model operates at a single scale."""

    def set_scaling_model(
        self,
        scaling: str,
        current_dir: str,
        device: str,
    ) -> None:
        """Configure the selected scaling model."""

    def create_model(self) -> None:
        """Load and initialise the scaling model."""
