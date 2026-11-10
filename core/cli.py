import argparse

from core.comparator import DEFAULT_WORK_SIZE
from core.tree import compare_images
from core.visualizer import render_heatmap


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare two images via binary spatial partitioning (BSP) trees."
    )
    parser.add_argument("image_a", help="Path to the first image")
    parser.add_argument("image_b", help="Path to the second image")
    parser.add_argument(
        "--min-block",
        type=int,
        default=6,
        help="Minimum block partition size in pixels (default: 6)",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=40.0,
        help="Color distance tolerance threshold (default: 40.0)",
    )
    parser.add_argument(
        "--work-size",
        type=int,
        default=DEFAULT_WORK_SIZE,
        help=f"Square processing resolution (default: {DEFAULT_WORK_SIZE})",
    )
    parser.add_argument(
        "--heatmap",
        type=str,
        default=None,
        help="Optional output path to save the diff heatmap PNG",
    )

    args = parser.parse_args()

    result = compare_images(
        args.image_a,
        args.image_b,
        min_block_size=args.min_block,
        tolerance=args.tolerance,
        work_size=args.work_size,
    )

    print(f"Similarity          : {result.similarity_percentage:.2f}%")
    print(f"Total pixels        : {result.total_pixels}")
    print(f"Matched pixels      : {result.matched_pixels}")
    print(f"Leaf blocks count   : {result.leaf_count}")
    print(f"Max tree depth      : {result.max_depth}")

    if args.heatmap:
        heatmap_image = render_heatmap(result, size=args.work_size)
        heatmap_image.save(args.heatmap)
        print(f"Heatmap saved to    : {args.heatmap}")