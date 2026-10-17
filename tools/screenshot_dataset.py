"""Capture screenshots of a screen region for dataset building.

Usage:
    python tools/screenshot_dataset.py --region minimap
    python tools/screenshot_dataset.py --region tank --interval 2 --out my_dir
"""
import argparse
import os
import time
from datetime import datetime

from PIL import Image

from tanksbot.config import MINIMAP, AimConfig

REGIONS = {
    "minimap": MINIMAP.monitor,
    "tank": AimConfig().monitor,
}

DEFAULT_OUTPUTS = {
    "minimap": "images-for-dataset/minimap-player",
    "tank": "images-for-dataset/tank-player",
}


def capture_loop(region: dict, out_dir: str, interval: float) -> None:
    """Save a screenshot of ``region`` every ``interval`` seconds until Ctrl+C."""
    import mss

    os.makedirs(out_dir, exist_ok=True)
    count = 0

    try:
        with mss.mss() as sct:
            while True:
                screenshot = sct.grab(region)
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(out_dir, f"screenshot_{timestamp}_{count}.png")
                img.save(filename)
                count += 1

                print(f"Скриншот сохранен: {filename}")
                time.sleep(interval)
    except KeyboardInterrupt:
        print("\nПрограмма остановлена")
        print(f"Всего сделано скриншотов: {count}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--region", choices=REGIONS, default="minimap",
                        help="which screen region to capture (default: minimap)")
    parser.add_argument("--out", default=None,
                        help="output folder (default: images-for-dataset/<region>-player)")
    parser.add_argument("--interval", type=float, default=3.0,
                        help="seconds between screenshots (default: 3)")
    args = parser.parse_args()

    out_dir = args.out or DEFAULT_OUTPUTS[args.region]
    capture_loop(REGIONS[args.region], out_dir, args.interval)


if __name__ == "__main__":
    main()
