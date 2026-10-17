"""YOLO model loading and target-selection helpers."""
from __future__ import annotations

import math
from pathlib import Path
from typing import List, Optional, Tuple

import cv2
import numpy as np
from ultralytics import YOLO

Box = Tuple[int, int, int, int]  # (x1, y1, x2, y2)


def load_model(path: Path | str) -> YOLO:
    """Load a YOLO model from disk."""
    return YOLO(str(path))


def find_closest_target(
    boxes,
    center_x: int,
    center_y: int,
    aim_height_frac: float = 5 / 8,
) -> Tuple[Optional[Tuple[int, int]], Optional[Box], float]:
    """Find the box whose aim point is closest to the given screen center.

    The aim point is the horizontal center of the box, placed
    ``aim_height_frac`` down from the top edge (tanks sit low in the box).

    Returns ``(aim_point, box, distance)``; ``(None, None, inf)`` if empty.
    """
    closest_dist = float("inf")
    aim_target: Optional[Tuple[int, int]] = None
    closest_box: Optional[Box] = None

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        box_h = y2 - y1

        cx = (x1 + x2) // 2
        cy = int(y1 + box_h * aim_height_frac)

        dist = math.hypot(cx - center_x, cy - center_y)
        if dist < closest_dist:
            closest_dist = dist
            aim_target = (cx, cy)
            closest_box = (x1, y1, x2, y2)

    return aim_target, closest_box, closest_dist


def draw_target_overlay(
    frame: np.ndarray,
    box: Box,
    target: Tuple[int, int],
    dist: float,
    shoot_dist: float,
    center: Tuple[int, int],
) -> None:
    """Draw the active target box, aim point, connecting line and labels."""
    x1, y1, x2, y2 = box
    tx, ty = target
    center_x, center_y = center

    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.circle(frame, (tx, ty), 5, (0, 0, 255), -1)
    cv2.line(frame, (center_x, center_y), (tx, ty), (0, 255, 255), 1)
    cv2.putText(
        frame, f"Dist: {dist:.1f}px", (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2,
    )
    if dist < shoot_dist:
        cv2.putText(
            frame, "SHOOTING!", (center_x - 50, center_y - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2,
        )


def draw_crosshair(frame: np.ndarray, center: Tuple[int, int]) -> None:
    """Draw the static crosshair at the screen center."""
    center_x, center_y = center
    cv2.circle(frame, (center_x, center_y), 3, (255, 255, 255), -1)
    cv2.circle(frame, (center_x, center_y), 10, (255, 255, 255), 1)
