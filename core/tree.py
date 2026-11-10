from __future__ import annotations

import numpy as np

from core.comparator import DEFAULT_WORK_SIZE, compare_block, load_image_as_array
from core.models import ComparisonResult, Node


def build_tree(
        arr_a: np.ndarray,
        arr_b: np.ndarray,
        min_block_size: int = 6,
        tolerance: float = 40.0,
) -> ComparisonResult:
    """Recursively split the image along its longest axis and evaluate the leaves."""
    h, w, _ = arr_a.shape
    total_pixels = 0
    matched_pixels = 0
    max_depth = 0
    leaf_count = 0

    def divide(x: int, y: int, width: int, height: int, depth: int) -> Node:
        nonlocal total_pixels, matched_pixels, max_depth, leaf_count
        max_depth = max(max_depth, depth)

        if width <= min_block_size and height <= min_block_size:
            block_a = arr_a[y : y + height, x : x + width]
            block_b = arr_b[y : y + height, x : x + width]
            total, matched = compare_block(block_a, block_b, tolerance)

            total_pixels += total
            matched_pixels += matched
            leaf_count += 1

            return Node(
                x=x,
                y=y,
                w=width,
                h=height,
                depth=depth,
                ratio=(matched / total if total else 1.0),
                total_pixels=total,
                matched_pixels=matched,
            )

        node = Node(x=x, y=y, w=width, h=height, depth=depth)
        if width >= height:
            mid_w = -(-width // 2)  # Ceiling division
            node.children = [
                divide(x, y, mid_w, height, depth + 1),
                divide(x + mid_w, y, width - mid_w, height, depth + 1),
            ]
        else:
            mid_h = -(-height // 2)
            node.children = [
                divide(x, y, width, mid_h, depth + 1),
                divide(x, y + mid_h, width, height - mid_h, depth + 1),
            ]
        return node

    root = divide(0, 0, w, h, 0)
    similarity = (matched_pixels / total_pixels * 100) if total_pixels else 0.0

    return ComparisonResult(
        root=root,
        similarity_percentage=similarity,
        total_pixels=total_pixels,
        matched_pixels=matched_pixels,
        leaf_count=leaf_count,
        max_depth=max_depth,
    )


def compare_images(image_a_path: str, image_b_path: str, min_block_size: int = 6,tolerance: float = 40.0,
        work_size: int = DEFAULT_WORK_SIZE,
) -> ComparisonResult:
    """High-level entry point: loads two images and evaluates spatial differences."""
    arr_a = load_image_as_array(image_a_path, work_size)
    arr_b = load_image_as_array(image_b_path, work_size)
    return build_tree(arr_a, arr_b, min_block_size=min_block_size, tolerance=tolerance)