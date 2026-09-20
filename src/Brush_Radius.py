class Brush_Radius:

    def adjust(self, brush_size: int, delta: int, minimum_brush_size: int) -> int:
        brush_size += delta

        brush_size = max(brush_size, minimum_brush_size)

        return brush_size
