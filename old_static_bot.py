"""Debug visualiser: detection boxes only, no aiming or input.

Usage:
    python old_static_bot.py

Press 'q' in the OpenCV window to quit.
"""
import cv2

from tanksbot.config import DEBUG_AIM
from tanksbot.detection import load_model
from tanksbot.screen import ScreenGrabber


def main() -> None:
    cfg = DEBUG_AIM
    model = load_model(cfg.model_path)
    grabber = ScreenGrabber(cfg.monitor)

    print("\nReady! Press 'q' in the window to exit...\n")

    while True:
        frame = grabber.grab()

        results = model(frame, verbose=False, conf=cfg.confidence, iou=cfg.iou)
        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        cv2.circle(frame, cfg.crosshair, 3, (255, 255, 255), -1)

        cv2.imshow(cfg.window_title, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    print("\nAimbot stopped.")


if __name__ == "__main__":
    main()
