from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QSlider, QStyle, QStyleOptionSlider


class Frame_Scrubber(QSlider):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.marker_frames: set[int] = set()

    def set_markers(self, frames: set[int]) -> None:
        self.marker_frames = frames
        self.update()

    def paintEvent(self, ev) -> None:
        super().paintEvent(ev)

        style = self.style()
        assert style is not None

        option = QStyleOptionSlider()
        self.initStyleOption(option)
        groove_rect = style.subControlRect(
            QStyle.ComplexControl.CC_Slider, option, QStyle.SubControl.SC_SliderGroove, self
        )
        handle_rect = style.subControlRect(
            QStyle.ComplexControl.CC_Slider, option, QStyle.SubControl.SC_SliderHandle, self
        )

        span = max(self.maximum() - self.minimum(), 1)
        travel = groove_rect.width() - handle_rect.width()
        painter = QPainter(self)
        painter.setPen(QColor("red"))

        for frame_index in self.marker_frames:
            ratio = (frame_index - self.minimum()) / span
            x = groove_rect.left() + int(ratio * travel) + handle_rect.width() // 2
            painter.drawLine(x, 0, x, self.height())
