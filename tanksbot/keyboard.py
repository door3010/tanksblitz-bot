"""Convert a grid path into tank key presses (W = forward, A/D = turn)."""
from __future__ import annotations

import time
from typing import List, Sequence, Tuple

import pydirectinput

DIRECTION_ORDER = ["UP", "RIGHT", "DOWN", "LEFT"]

# Key hold times, in seconds.
MOVE_STEP_DELAY = 0.5
TURN_STEP_DELAY = 1.25


def get_turn_sequence(current_dir: str, target_dir: str) -> List[str]:
    """Return the A/D presses needed to turn from ``current_dir`` to ``target_dir``."""
    curr_idx = DIRECTION_ORDER.index(current_dir)
    targ_idx = DIRECTION_ORDER.index(target_dir)
    diff = (targ_idx - curr_idx) % 4
    if diff == 0:
        return []
    if diff == 1:
        return ["d"]
    if diff == 2:
        return ["d", "d"]
    return ["a"]


def get_target_direction(dy: int, dx: int) -> str | None:
    """Cardinal direction for a single-axis step."""
    if dx > 0:
        return "RIGHT"
    if dx < 0:
        return "LEFT"
    if dy > 0:
        return "DOWN"
    if dy < 0:
        return "UP"
    return None


def build_commands(path: Sequence[Sequence[int]], initial_direction: str = "UP") -> Tuple[str, List[str]]:
    """Turn a list of grid cells into a flat sequence of key presses.

    Returns ``(facing_direction_after_last_step, commands)``.
    """
    if len(path) < 2:
        return initial_direction, []

    facing = initial_direction
    commands: List[str] = []
    pos = path[0]

    for nxt in path[1:]:
        dy = nxt[0] - pos[0]
        dx = nxt[1] - pos[1]
        if dx == 0 and dy == 0:
            continue

        # Diagonal steps are split into two axis-aligned moves.
        if dx != 0 and dy != 0:
            segments = [("x", dx), ("y", dy)]
        elif dx != 0:
            segments = [("x", dx)]
        else:
            segments = [("y", dy)]

        for axis, delta in segments:
            if delta == 0:
                continue
            target = get_target_direction(dy if axis == "y" else 0, dx if axis == "x" else 0)
            commands.extend(get_turn_sequence(facing, target))
            facing = target
            commands.extend(["w"] * abs(delta))

        pos = nxt

    return facing, commands


def execute_commands(commands: Sequence[str]) -> None:
    """Physically press the keys with the configured hold times."""
    for key in commands:
        pydirectinput.keyDown(key)
        time.sleep(MOVE_STEP_DELAY if key == "w" else TURN_STEP_DELAY)
        pydirectinput.keyUp(key)


def execute_path(
    path: Sequence[Sequence[int]],
    initial_direction: str = "UP",
    dry_run: bool = False,
) -> Tuple[str, List[str]]:
    """Build and (unless ``dry_run``) execute the key sequence for ``path``.

    Returns ``(facing_direction, commands)``. Short or empty paths are a
    no-op instead of an error.
    """
    facing, commands = build_commands(path, initial_direction)
    if not commands:
        print("Path too short.")
        return facing, commands
    if not dry_run:
        execute_commands(commands)
    return facing, commands
