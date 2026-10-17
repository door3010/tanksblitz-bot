import cv2
import numpy as np
import mss
import math
from config import  Minimap

# --- 1. Define the minimap region (x, y, width, height) ---
# Adjust these values to match your minimap's position on screen
MINIMAP_REGION = Minimap.monitor

# --- 2. Define the arrow's color range in HSV ---
# Tweak these based on your arrow's color. Example: yellow/orange arrow
UPPER_COLOR = np.array([223, 249, 247])   # lower HSV bound
LOWER_COLOR = np.array([128, 163, 159])   # upper HSV bound


def capture_minimap():
    """Capture the minimap region using mss."""
    with mss.mss() as sct:
        img = np.array(sct.grab(MINIMAP_REGION))
        # mss returns BGRA; convert to BGR then HSV
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


def find_arrow_angle(bgr_image):
    """Return the arrow's angle in degrees (0 = East, counter-clockwise)."""
    hsv = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, LOWER_COLOR, UPPER_COLOR)

    # Clean up noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None, None, mask

    # Pick the largest contour (assumed to be the arrow)
    arrow = max(contours, key=cv2.contourArea)

    # minAreaRect returns ((cx, cy), (w, h), angle)
    # angle is between -90 and 0 for OpenCV; we normalize it
    rect = cv2.minAreaRect(arrow)
    angle = rect[2]

    # OpenCV's angle is the rotation of the width side.
    # If width < height, the "long axis" is actually rotated 90° from `angle`.
    (w, h) = rect[1]
    if w < h:
        angle += 90

    # Now `angle` is in degrees, 0 = pointing right (East), CCW positive.
    return angle, rect, mask


def angle_to_compass(angle_deg):
    """Convert math angle (0=East, CCW) to compass direction (0=North, CW)."""
    # Convert: compass = 90 - math_angle
    compass = (90 - angle_deg) % 360
    dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    idx = int((compass + 22.5) // 45) % 8
    return dirs[idx], compass


def main():
    while True:
        bgr = capture_minimap()
        angle, rect, mask = find_arrow_angle(bgr)

        if angle is None:
            print("Arrow not found — adjust color range or region.")
        else:
            direction, compass = angle_to_compass(angle)
            print(f"Angle: {angle:6.1f}°  |  Compass: {compass:6.1f}°  |  Dir: {direction}")

            # Draw the arrow's orientation on the image for debugging
            center = (int(rect[0][0]), int(rect[0][1]))
            # Draw a line showing the detected direction
            rad = math.radians(angle)
            length = 60
            end = (int(center[0] + length * math.cos(rad)),
                   int(center[1] - length * math.sin(rad)))
            cv2.arrowedLine(bgr, center, end, (0, 255, 0), 2, tipLength=0.15)
            cv2.circle(bgr, center, 3, (0, 0, 255), -1)

        # Show debug windows
        cv2.imshow("Minimap", bgr)
        cv2.imshow("Mask", mask)

        if cv2.waitKey(30) & 0xFF == 27:  # ESC to quit
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()