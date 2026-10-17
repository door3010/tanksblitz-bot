"""Debug visualisation helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

from PIL import Image

from tanksbot.config import PROJECT_ROOT

DEFAULT_MINIMAP_IMAGE = PROJECT_ROOT / "true-bw-minimap.png"
DEFAULT_OUTPUT_IMAGE = PROJECT_ROOT / "bw-minimap-with-path.png"


def draw_path(
    path: Sequence[Sequence[int]],
    source_image: Path | str = DEFAULT_MINIMAP_IMAGE,
    output_image: Path | str = DEFAULT_OUTPUT_IMAGE,
) -> Path:
    """Paint the computed path (green) onto the black-and-white minimap.

    Args:
        path: cells as ``(row, col)``.
        source_image: background minimap image.
        output_image: where the result is written.

    Returns:
        The output image path.
    """
    image = Image.open(source_image).convert("RGBA")
    for row, col in path:
        image.putpixel((col, row), (0, 255, 0, 255))
    image.save(output_image)
    return Path(output_image)
