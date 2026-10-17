"""Minimap maze and shortest-path (BFS) computation.

The maze is a binary grid generated from ``true-bw-minimap.png`` by
``tools/make_maze_config.py``; the data lives in ``tanksbot/maze_data.py``.
Convention: ``0`` = passable, ``1`` = wall. Coordinates are ``(row, col)``.
"""
from __future__ import annotations

from collections import deque
from typing import List, Optional, Sequence, Tuple

import numpy as np

from tanksbot.maze_data import MAZE_STR

Coord = Tuple[int, int]


def _parse_maze(maze_str: str) -> np.ndarray:
    return np.array([[int(ch) for ch in row] for row in maze_str.strip().splitlines()], dtype=int)


MAZE: np.ndarray = _parse_maze(MAZE_STR)


def shortest_path(
    src: Sequence[int],
    dest: Sequence[int],
    maze: np.ndarray = MAZE,
) -> Optional[List[Coord]]:
    """Breadth-first shortest path on the maze grid.

    Args:
        src: start cell ``(row, col)``.
        dest: target cell ``(row, col)``.
        maze: binary grid, 0 = passable.

    Returns:
        List of cells from ``src`` to ``dest`` inclusive, or ``None`` if
        either endpoint is a wall or no path exists.
    """
    n, m = maze.shape
    src_t = (int(src[0]), int(src[1]))
    dest_t = (int(dest[0]), int(dest[1]))

    for r, c in (src_t, dest_t):
        if not (0 <= r < n and 0 <= c < m) or maze[r][c] == 1:
            return None

    queue: deque[Coord] = deque([src_t])
    parent: dict = {src_t: None}
    steps = ((-1, 0), (1, 0), (0, -1), (0, 1))

    while queue:
        x, y = queue.popleft()
        if (x, y) == dest_t:
            path: List[Coord] = []
            curr: Optional[Coord] = (x, y)
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            return path[::-1]

        for dx, dy in steps:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == 0 and (nx, ny) not in parent:
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    return None
