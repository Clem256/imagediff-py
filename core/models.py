from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Node:
    """
    A node within the binary spatial partitioning (BSP) tree.

    Params:
        x (int): Horizontal origin coordinate (left) of the block in pixels.
        y (int): Vertical origin coordinate (top) of the block in pixels.
        w (int): Width of the block in pixels.
        h (int): Height of the block in pixels.
        depth (int): Depth of this node in the tree (0 for the root).
        children (List[Node]): Sub-regions resulting from the split. Empty for leaves.
        ratio (Optional[float]): Match score for terminal leaf nodes, in the range [0.0, 1.0].
            Calculated as `matched_pixels / total_pixels`.
            - 1.0: 100% of pixels match within tolerance (rendered Green in the heatmap).
            - 0.5: 50% match (rendered Yellow).
            - 0.0: No pixels match within tolerance (rendered Red).
            Remains `None` for internal branch nodes.
        total_pixels (int): Total pixel count in this leaf (`w * h`). 0 for internal nodes.
        matched_pixels (int): Count of pixels matching within tolerance. 0 for internal nodes.
    """
    x: int
    y: int
    w: int
    h: int
    depth: int
    children: List["Node"] = field(default_factory=list)
    ratio: Optional[float] = None
    total_pixels: int = 0
    matched_pixels: int = 0

    @property
    def is_leaf(self):
        """
        Return True if this node is a terminal leaf (has no sub-blocks).
        """
        return not self.children


@dataclass
class ComparisonResult:
    """
    Aggregated outcome of an image comparison across the full partitioning tree.

    Params:
        root (Node): Root node of the binary spatial partitioning (BSP) tree.
        similarity_percentage (float): Global match score across the whole image,
            ranging from 0.0 to 100.0%.
            Calculated as `(matched_pixels / total_pixels) * 100`.
        total_pixels (int): Overall count of pixels evaluated across all leaves.
            Matches the processing resolution squared (e.g., 256 * 256 = 65,536).
        matched_pixels (int): Total count of pixels across all leaves satisfying
            the color distance tolerance threshold.
        leaf_count (int): Number of terminal blocks produced by the recursive split.
            Reflects the granularity of the spatial breakdown.
        max_depth (int): Maximum depth reached by the tree during recursion
            (0 indicates no splits occurred).
    """
    root: Node
    similarity_percentage: float
    total_pixels: int
    matched_pixels: int
    leaf_count: int
    max_depth: int

    def leaves(self) -> List[Node]:
        """
        Traverse the tree depth-first and return all terminal leaf nodes.

        Returns:
            List[Node]: A flat list of leaves, each containing comparison metrics
            (`ratio`, `matched_pixels`, `total_pixels`) used for rendering heatmaps.
        """
        leaf_nodes: List[Node] = []

        def walk(node: Node) -> None:
            if node.is_leaf:
                leaf_nodes.append(node)
            else:
                for child in node.children:
                    walk(child)

        walk(self.root)
        return leaf_nodes
