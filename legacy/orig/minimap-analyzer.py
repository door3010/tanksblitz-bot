import cv2
import numpy as np
import mss
from ultralytics import YOLO
from config import  Minimap
from draw_path import draw_path
from path_reader_keyboard_output import execute_path
from shortest_path_calculation import shortestPath
dest=[73, 157]
model = YOLO(Minimap.arrow_model_path)
initial_direction="UP"
print("Starting detection... Press 'q' in the OpenCV window to quit.")
import pygetwindow as gw

handle = gw.getWindowsWithTitle('Tanks Blitz')[0]
handle.resizeTo(800, 600)
handle.moveTo(-5,0)
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
        x1, y1, x2, y2, x3, y3, x4, y4 = box.xyxyxyxy[0].tolist()
        screen_x1 = x1 + Minimap.monitor["left"]
        screen_y1 = y1 + Minimap.monitor["top"]
        screen_x2 = x2 + Minimap.monitor["left"]
        screen_y2 = y2 + Minimap.monitor["top"]

        # cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        cv2.line(frame, (int(x1), int(y1)), (int(x3), int(y3)), (0, 255, 0), 2)
        cv2.line(frame, (int(x2), int(y2)), (int(x4), int(y4)), (0, 255, 0), 2)
        cv2.line(frame, (int(x3), int(y3)), (int(x4), int(y4)), (0, 255, 0), 2)
        player_pos_x = (int(x1)+int(x2))/2
        player_pos_y = (int(y1)+int(y2))/2
        if dest[0] is not None:
            path_list_of_nodes = shortestPath([int(player_pos_y), int(player_pos_x)], dest)
            print(path_list_of_nodes)
            initial_direction, _ = execute_path(path_list_of_nodes, initial_direction=initial_direction, dry_run=False)
            draw_path(path_list_of_nodes)
            dest[0]= None
    cv2.imshow("Minimap Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()