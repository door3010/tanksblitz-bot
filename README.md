# Tanks Blitz Bot

Computer-vision bot for Tanks Blitz: a YOLO-based aimbot plus minimap
navigation (arrow detection → BFS pathfinding → keyboard control).

## Structure

```
tanksblitz-bot/
├── tanksbot/               # core package
│   ├── config.py           # all settings (aimbot, minimap, debug)
│   ├── maze_data.py        # generated minimap maze grid (MAZE_STR)
│   ├── screen.py           # screen capture (mss) + game window positioning
│   ├── detection.py        # YOLO loading, target selection, overlays
│   ├── pathing.py          # maze + BFS shortest path
│   ├── keyboard.py         # grid path -> W/A/D key presses
│   ├── visualize.py        # path rendering on the minimap image
│   └── aimbot.py           # main aimbot loop
├── bot.py                  # aimbot entry point
├── minimap_analyzer.py     # navigation entry point
├── minimap_grabber.py      # minimap debug preview
├── calibration.py          # interactive HSV arrow calibration
├── old_static_bot.py       # detection-only visualiser
├── config.py               # legacy shim (AimTank / Minimap names)
├── tools/                  # utilities
│   ├── screenshot_dataset.py   # dataset screenshots (minimap|tank region)
│   ├── make_maze_config.py     # regenerate tanksbot/maze_data.py
│   ├── pick_coordinates.py     # click-to-get pixel coordinates
│   └── check_dependencies.py   # import verification
└── legacy/                 # archived pre-refactor code (orig/ = originals)
```

## Setup

```
pip install -r requirements.txt
```

Run `python tools/check_dependencies.py` to verify the environment.

## Datasets

The training data and captured screenshots are not committed to the repository.
Download the archives and extract them at the project root:

| Archive | Contents | Extract to |
|---|---|---|
| [datasets.zip](https://drive.google.com/file/d/1Xe_GmfW6BVK3BN1Op5cx4NYkq0DhnZjd/view?usp=sharing) | YOLO datasets: `arrow`, `buildings-set`, `e5`, `fixed-classes` | `datasets/` |
| [images-for-dataset.zip](https://drive.google.com/file/d/17_izWDna1cXgpmGC6yWl_plxETChuAeK/view?usp=sharing) | Captured screenshots: `minimap-player`, `tank-player` | `images-for-dataset/` |

Both directories are listed in `.gitignore`. The maze source image
`true-bw-minimap.png` is already included in the repository.

Model weights are not included either; `tanksbot/config.py` expects them under
`runs/segment/<run>/weights/best.pt`.

## Usage

| Script | Purpose |
|---|---|
| `python bot.py` | Aimbot (aims at the closest target, optional auto-fire). Press `q` to quit. |
| `python minimap_analyzer.py` | Detects the player arrow, plans a path to the configured destination and drives the tank. |
| `python minimap_grabber.py` | Debug view of the minimap with detection + binary threshold. |
| `python calibration.py` | Interactive HSV range tuning for the arrow colour (ESC to quit). |
| `python old_static_bot.py` | Detection boxes only, no input. |

## Tools

```
python tools/screenshot_dataset.py --region minimap --interval 3
python tools/screenshot_dataset.py --region tank --out images-for-dataset/tank-player
python tools/make_maze_config.py        # after editing true-bw-minimap.png
python tools/pick_coordinates.py [image]  # click to print (x, y)
```

## Configuration

All tunables live in `tanksbot/config.py`:

- `AIM` — main aimbot (model, capture region, smoothing, auto-fire distance)
- `DEBUG_AIM` — detection-only visualiser
- `MINIMAP` — arrow model, minimap region, game window geometry, default destination `(row, col)`

Paths are resolved relative to the project root; the maze grid is generated
from `true-bw-minimap.png` into `tanksbot/maze_data.py`.

## Notes

- Screen coordinates: capture regions are mss dicts (`left/top/width/height`).
- Minimap navigation uses `(row, col)` grid coordinates; the maze treats
  `0` as passable and `1` as a wall.
- Pre-refactor scripts are preserved in `legacy/orig/`.
