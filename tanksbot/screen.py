"""Screen capture and game window helpers."""
from __future__ import annotations

from typing import Dict

import cv2
import mss
import numpy as np


class ScreenGrabber:
    """Grabs a fixed screen region and returns OpenCV frames.

    The mss instance is created once and reused, which is both faster and
    required to avoid thread/connection issues with repeated mss.mss() calls.
    """

    def __init__(self, monitor: Dict[str, int]):
        self.monitor = monitor
        self._sct = mss.mss()

    def grab(self) -> np.ndarray:
        """Grab the configured region and return a BGR uint8 array."""
        frame = np.array(self._sct.grab(self.monitor))
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    def grab_gray(self) -> np.ndarray:
        """Grab the configured region and return a grayscale uint8 array."""
        frame = np.array(self._sct.grab(self.monitor))
        return cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)


def position_game_window(
    title: str = "Tanks Blitz",
    width: int = 800,
    height: int = 600,
    x: int = -5,
    y: int = 0,
) -> None:
    """Resize and move the game window so screen coordinates match the config."""
    import pygetwindow as gw

    windows = gw.getWindowsWithTitle(title)
    if not windows:
        raise RuntimeError(f"Game window not found: {title!r}")
    handle = windows[0]
    handle.resizeTo(width, height)
    handle.moveTo(x, y)
