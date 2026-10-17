"""Regenerate the minimap maze data from the black-and-white minimap image.

Usage:
    python tools/make_maze_config.py

Reads ``true-bw-minimap.png`` and writes ``tanksbot/maze_data.py``.
"""
from pathlib import Path

import numpy as np
from PIL import Image

from tanksbot.config import PROJECT_ROOT

SOURCE_IMAGE = PROJECT_ROOT / "true-bw-minimap.png"
OUTPUT_FILE = PROJECT_ROOT / "tanksbot" / "maze_data.py"


def main() -> None:
    image = Image.open(SOURCE_IMAGE).convert("L")
    binary = image.point(lambda p: 1 if p > 128 else 0)
    binary = binary.resize(image.size, Image.NEAREST)

    maze = np.array(binary)
    maze_str = "\n".join("".join(str(cell) for cell in row) for row in maze)

    OUTPUT_FILE.write_text(f'MAZE_STR = """\n{maze_str}\n"""\n', encoding="utf-8")
    print(f"Grid size: {maze.shape[0]}x{maze.shape[1]}")
    print(f"Written: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
