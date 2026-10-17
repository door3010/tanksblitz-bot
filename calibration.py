"""Interactive HSV calibration for the minimap arrow colour.

Usage:
    python calibration.py

Shows the minimap and its colour mask; press ESC to quit.
Print the printed HSV bounds into ``tanksbot/calibration`` usage as needed.
"""
import math

import cv2
import numpy as np

from tanksbot.config import MINIMAP
from tanksbot.screen import ScreenGrabber

# HSV bounds of the arrow colour (inclusive range for cv2.inRange).
HSV_LOW = np.array([128, 163, 159])
HSV_HIGH = np.array([223, 249, 247])

COMPASS_DIRS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def find_arrow_angle(bgr_image: np.ndarray):
    """Return ``(angle_deg, min_area_rect, mask)`` for the largest blob.

    ``angle_deg``: 0 = East, counter-clockwise positive. ``None`` if not found.
    """
    hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, HSV_LOW, HSV_HIGH)

    # Clean up noise.
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None, mask

    arrow = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(arrow)
    angle = rect[2]

    # OpenCV reports the rotation of the width side; if the height is the
    # longer side, the actual long-axis angle is rotated by 90 degrees.
    w, h = rect[1]
    if w < h:
        angle += 90

    return angle, rect, mask


def angle_to_compass(angle_deg: float):
    """Convert math angle (0=East, CCW) to compass direction (0=N, CW)."""
    compass = (90 - angle_deg) % 360
    idx = int((compass + 22.5) // 45) % 8
    return COMPASS_DIRS[idx], compass


def main() -> None:
    grabber = ScreenGrabber(MINIMAP.monitor)

    while True:
        bgr = grabber.grab()
        angle, rect, mask = find_arrow_angle(bgr)

        if angle is None:
            print("Arrow not found — adjust color range or region.")
        else:
            direction, compass = angle_to_compass(angle)
            print(f"Angle: {angle:6.1f}°  |  Compass: {compass:6.1f}°  |  Dir: {direction}")

            # Draw the detected direction for debugging.
            center = (int(rect[0][0]), int(rect[0][1]))
            rad = math.radians(angle)
            length = 60
            end = (
                int(center[0] + length * math.cos(rad)),
                int(center[1] - length * math.sin(rad)),
            )
            cv2.arrowedLine(bgr, center, end, (0, 255, 0), 2, tipLength=0.15)
            cv2.circle(bgr, center, 3, (0, 0, 255), -1)

        cv2.imshow("Minimap", bgr)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(30) & 0xFF == 27:  # ESC to quit
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
