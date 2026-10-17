"""Main aimbot loop: capture screen -> detect tanks -> aim and shoot."""
from __future__ import annotations

import cv2
import win32api
import win32con

from tanksbot.config import AimConfig
from tanksbot.detection import (
    draw_crosshair,
    draw_target_overlay,
    find_closest_target,
    load_model,
)
from tanksbot.screen import ScreenGrabber


def move_mouse_relative(dx: int, dy: int) -> None:
    """Move the mouse by a relative amount using the Win32 API."""
    if dx != 0 or dy != 0:
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)


def shoot() -> None:
    """Left click (fire)."""
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def run_aimbot(config: AimConfig = None) -> None:
    """Run the aimbot until 'q' is pressed in the preview window."""
    config = config or AimConfig()
    center = (config.center_x, config.center_y)

    print("=" * 50)
    print("Tanks Blitz Aimbot - Starting...")
    print(f"Model:  {config.mle_model_path}")
    print(f"Monitor: {config.monitor['width']}x{config.monitor['height']}")
    print(f"Center: {center}")
    print(f"Smoothing: {config.smoothing}")
    print(f"Auto-shoot distance: {config.shoot_dist}px")
    print("Press 'q' to quit")
    print("=" * 50)

    model = load_model(config.mle_model_path)
    grabber = ScreenGrabber(config.monitor)
    prev_tick = cv2.getTickCount()

    print("\n✅ Ready! Press 'q' in the window to exit...\n")

    while True:
        frame = grabber.grab()

        results = model(
            frame,
            verbose=False,
            conf=config.confidence,
            iou=config.iou,
        )

        aim_target, closest_box, closest_dist = find_closest_target(
            results[0].boxes, config.center_x, config.center_y, config.aim_height_frac
        )

        if aim_target and closest_box:
            tx, ty = aim_target

            # Relative mouse move with smoothing.
            move_mouse_relative(
                int((tx - config.center_x) * config.smoothing),
                int((ty - config.center_y) * config.smoothing),
            )

            if config.auto_shoot and closest_dist < config.shoot_dist:
                shoot()

            draw_target_overlay(
                frame, closest_box, aim_target, closest_dist, config.shoot_dist, center
            )

        draw_crosshair(frame, center)

        # FPS from the delta between frames.
        now = cv2.getTickCount()
        fps = (now - prev_tick) / cv2.getTickFrequency()
        prev_tick = now
        cv2.putText(
            frame, f"FPS: {1 / fps:.1f}", (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2,
        )

        cv2.imshow(config.window_title, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    print("\n👋 Aimbot stopped.")


if __name__ == "__main__":
    run_aimbot()
