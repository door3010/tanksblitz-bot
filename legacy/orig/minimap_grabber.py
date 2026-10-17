import cv2
import numpy as np
import mss
from ultralytics import YOLO
from config import  Minimap
model = YOLO(Minimap.arrow_model_path)
import pygetwindow as gw

handle = gw.getWindowsWithTitle('Tanks Blitz')[0]
handle.resizeTo(800, 600)
handle.moveTo(-5,0)
sct = mss.mss()

def grab_image_needed_size(monitor_size):
    sct_img = sct.grab(monitor_size)
    frame_np = np.array(sct_img)
    frame = cv2.cvtColor(frame_np, cv2.COLOR_BGR2GRAY)
    return frame

while True:
    frame = grab_image_needed_size(Minimap.monitor)
    results = model(frame, conf=0.5, verbose=False)
    for box in results[0].boxes:
        x1, y1, x2, y2= box.xyxy[0].tolist()
        screen_x1 = x1 + Minimap.monitor["left"]
        screen_y1 = y1 + Minimap.monitor["top"]
        screen_x2 = x2 + Minimap.monitor["left"]
        screen_y2 = y2 + Minimap.monitor["top"]

        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    frame = cv2.threshold(frame, 170, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow("Minimap Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()