import cv2
import numpy as np
import mss
from ultralytics import YOLO

from config import  Minimap
from mss_screen_grabber import ScreenGrabber

# 1. Load your YOLOv8 model
model = YOLO(Minimap.arrow_model_path)

print("Starting detection... Press 'q' in the OpenCV window to quit.")
sct = mss.mss()
def grab_image_needed_size(monitor_size):
    sct_img = sct.grab(monitor_size)
    frame_np = np.array(sct_img)
    frame = cv2.cvtColor(frame_np, cv2.COLOR_BGRA2BGR)
    return frame

while True:
    frame = grab_image_needed_size(Minimap.monitor)
    results = model(frame, conf=0.5, verbose=False)

    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        confidence = box.conf[0].item()
        cls = int(box.cls[0].item())

        screen_x1 = x1 + Minimap.monitor.minimap_left
        screen_y1 = y1 + Minimap.monitor.minimap_top
        screen_x2 = x2 + Minimap.monitor.minimap_left
        screen_y2 = y2 + Minimap.monitor.minimap_top

        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    cv2.imshow("Minimap Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()