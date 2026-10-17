"""Minimap grabber with arrow detection and binary-threshold preview.

Usage:
    python minimap_grabber.py

Press 'q' in the OpenCV window to quit.
"""
import cv2

from tanksbot.config import MINIMAP
from tanksbot.detection import load_model
from tanksbot.screen import ScreenGrabber, position_game_window

THRESHOLD_VALUE = 170


def main() -> None:
    cfg = MINIMAP

    position_game_window(
        cfg.game_window_title,
        cfg.game_window_width,
        cfg.game_window_height,
        cfg.game_window_x,
        cfg.game_window_y,
    )

    model = load_model(cfg.arrow_model_path)
    grabber = ScreenGrabber(cfg.monitor)

    while True:
        frame = grabber.grab_gray()
        results = model(frame, conf=cfg.confidence, verbose=False)

        # Threshold first, then draw boxes so they stay visible.
        display = cv2.threshold(frame, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)[1]
        display = cv2.cvtColor(display, cv2.COLOR_GRAY2BGR)

        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cv2.rectangle(display, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        cv2.imshow("Minimap Detection", display)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
