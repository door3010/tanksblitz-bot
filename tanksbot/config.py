"""Central configuration for the Tanks Blitz bot.

All paths are resolved relative to the project root, so the project can be
moved to another machine without editing absolute paths.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _monitor(left: int, top: int, width: int, height: int) -> Dict[str, int]:
    """Build an mss-compatible monitor dict."""
    return {"left": left, "top": top, "width": width, "height": height}


@dataclass(frozen=True)
class AimConfig:
    """Settings for the main aimbot (bot.py)."""

    mle_model_path: Path = PROJECT_ROOT / "runs" / "segment" / "mle_cpu_run" / "weights" / "best.pt"
    monitor: Dict[str, int] = field(default_factory=lambda: _monitor(0, 30, 800, 410))
    center_x: int = 400
    center_y: int = 300
    smoothing: float = 0.15          # mouse sensitivity factor (0.1-0.3)
    aim_height_frac: float = 5 / 8   # aim point as a fraction of the box height
    shoot_dist: float = 50           # auto-fire distance from screen center, px
    auto_shoot: bool = True
    confidence: float = 0.5
    iou: float = 0.45
    window_title: str = "Tanks Blitz Aimbot"


@dataclass(frozen=True)
class DebugAimConfig:
    """Settings for the debug visualiser (old_static_bot.py): detection only."""

    model_path: Path = PROJECT_ROOT / "runs" / "segment" / "e5_cpu_run" / "weights" / "best.pt"
    monitor: Dict[str, int] = field(default_factory=lambda: _monitor(100, 100, 1720, 660))
    confidence: float = 0.5
    iou: float = 0.45
    crosshair: tuple = (960, 480)
    window_title: str = "Tanks Blitz Aimbot"


@dataclass(frozen=True)
class MinimapConfig:
    """Settings for minimap navigation (minimap_analyzer.py, minimap_grabber.py)."""

    arrow_model_path: Path = PROJECT_ROOT / "runs" / "segment" / "arrow_cpu_run-2" / "weights" / "best.pt"
    monitor: Dict[str, int] = field(default_factory=lambda: _monitor(0, 390, 200, 200))
    confidence: float = 0.5
    # Position/size of the game window used by the navigation pipeline.
    game_window_title: str = "Tanks Blitz"
    game_window_width: int = 800
    game_window_height: int = 600
    game_window_x: int = -5
    game_window_y: int = 0
    # Default navigation target as (row, col) on the minimap grid.
    default_destination: tuple = (73, 157)


# Ready-to-use singletons.
AIM = AimConfig()
DEBUG_AIM = DebugAimConfig()
MINIMAP = MinimapConfig()
