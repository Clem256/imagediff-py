import numpy as np
from PIL import Image

DEFAULT_WORK_SIZE = 256


def load_image_as_array(path: str, size: int = DEFAULT_WORK_SIZE):
    """
    Load an image, convert it to RGB, and resize to a square size x size array.
    """
    image = Image.open(path).convert("RGB").resize((size, size), Image.LANCZOS)
    return np.asarray(image, dtype=np.int16)  # int16 prevents overflow during subtraction


def compare_block(a: np.ndarray, b: np.ndarray, tolerance: float) -> tuple[int, int]:
    """Compare two image blocks pixel by pixel.

    Returns:
        tuple[int, int]: (total_pixels, matching_pixels)
    """
    diff = a - b
    distance = np.sqrt((diff.astype(np.float32) ** 2).sum(axis=-1))
    matched = int((distance <= tolerance).sum())
    total = a.shape[0] * a.shape[1]
    return total, matched
