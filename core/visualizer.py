from PIL import Image

from core.comparator import DEFAULT_WORK_SIZE
from core.models import ComparisonResult


def render_heatmap(result: ComparisonResult, size: int = DEFAULT_WORK_SIZE) -> Image.Image:
    """Generate a heatmap image: red for differences, green for matches."""
    canvas = Image.new("RGB", (size, size))
    pixels = canvas.load()

    def get_color_for_ratio(ratio: float) -> tuple[int, int, int]:
        # Gradient stops: Red -> Yellow -> Green
        color_stops = [(255, 93, 93), (233, 210, 92), (52, 214, 122)]
        clamped_t = max(0.0, min(1.0, ratio)) * 2
        segment_idx = 1 if clamped_t >= 1 else 0
        local_t = clamped_t - segment_idx
        start_color, end_color = color_stops[segment_idx], color_stops[segment_idx + 1]

        return tuple( int(start_color[i] + (end_color[i] - start_color[i]) * local_t) for i in range(3))

    for leaf in result.leaves():
        block_color = get_color_for_ratio(leaf.ratio or 0.0)
        for row in range(leaf.y, min(leaf.y + leaf.h, size)):
            for col in range(leaf.x, min(leaf.x + leaf.w, size)):
                pixels[col, row] = block_color

    return canvas