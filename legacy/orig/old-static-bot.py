import cv2
import numpy as np
import mss
import win32api
import win32con
import math
from ultralytics import YOLO

from config import AimTank

model = YOLO(AimTank.e5_model_path)

with mss.mss() as sct:
    print("\nReady! Press 'q' in the window to exit...\n")

    while True:
        sct_img = sct.grab(AimTank.monitor)
        frame = np.array(sct_img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        results = model(frame, verbose=False, conf=AimTank.CONFIDENCE_THRESHOLD, iou=AimTank.IOU_THRESHOLD)

        for box in results[0].boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

            # 6. Отрисовка центра прицела
        cv2.circle(frame, (1920//2, 960//2), 3, (255, 255, 255), -1)

        cv2.imshow("Tanks Blitz Aimbot", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
print("\nAimbot stopped.")