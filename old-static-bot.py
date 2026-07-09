import cv2
import numpy as np
import mss
import win32api
import win32con
import math
from ultralytics import YOLO

from config import AimTank

# Загрузка модели
model = YOLO(AimTank.mle_model_path)


def find_closest_target(boxes, center_x, center_y):
    """Находит ближайшую к центру экрана цель"""
    closest_dist = float('inf')
    aim_target = None
    closest_box = None

    for box in boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        box_h = y2 - y1

        # Центр бокса с поправкой на высоту
        cx = int((x1 + x2) / 2)
        cy = int(y1 + (box_h * 5 /8))

        # Расстояние от центра экрана до цели
        dist = math.sqrt((cx - center_x) ** 2 + (cy - center_y) ** 2)

        if dist < closest_dist:
            closest_dist = dist
            aim_target = (cx, cy)
            closest_box = (x1, y1, x2, y2)

    return aim_target, closest_box, closest_dist


with mss.mss() as sct:
    print("\n✅ Ready! Press 'q' in the window to exit...\n")

    while True:
        # 1. Захват экрана
        sct_img = sct.grab(AimTank.monitor)
        frame = np.array(sct_img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        # 2. Детекция объектов
        results = model(frame, verbose=False, conf=AimTank.CONFIDENCE_THRESHOLD, iou=AimTank.IOU_THRESHOLD)

        # 3. Инициализация переменных
        aim_target = None
        closest_dist = float('inf')
        closest_box = None

        # 4. Обработка результатов
        for result in results:
            boxes = result.boxes

            if len(boxes) > 0:
                # Найти ближайшую к центру цель
                aim_target, closest_box, closest_dist = find_closest_target(
                    boxes, AimTank.CENTER_X, AimTank.CENTER_Y
                )

        # 5. Прицеливание и стрельба
        if aim_target and closest_box:
            tx, ty = aim_target
            x1, y1, x2, y2 = closest_box

            # Рассчитать смещение от текущего положения
            # (win32api.mouse_event с MOUSEEVENTF_MOVE использует относительные координаты)
            offset_x = tx - AimTank.CENTER_X
            offset_y = ty - AimTank.CENTER_Y

            # Применить сглаживание
            move_x = int(offset_x * AimTank.SMOOTHING)
            move_y = int(offset_y * AimTank.SMOOTHING)

            # Движение мыши через Windows API
            if move_x != 0 or move_y != 0:
                win32api.mouse_event(
                    win32con.MOUSEEVENTF_MOVE,
                    move_x,
                    move_y,
                    0, 0
                )

            # Авто-выстрел если цель достаточно близко к центру
            if AimTank.AUTO_SHOOT and closest_dist < AimTank.SHOOT_DIST:
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                # Небольшая задержка между выстрелами (опционально)
                # time.sleep(0.1)

            # Отрисовка bounding box (зелёный - активная цель)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Отрисовка точки прицеливания (красная)
            cv2.circle(frame, (tx, ty), 5, (0, 0, 255), -1)

            # Отрисовка линии от центра к цели
            cv2.line(frame, (AimTank.CENTER_X, AimTank.CENTER_Y), (tx, ty), (0, 255, 255), 1)

            # Информация о цели
            cv2.putText(frame, f"Dist: {closest_dist:.1f}px", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if closest_dist < AimTank.SHOOT_DIST:
                cv2.putText(frame, "SHOOTING!", (AimTank.CENTER_X - 50, AimTank.CENTER_Y - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        # 6. Отрисовка центра прицела
        cv2.circle(frame, (AimTank.CENTER_X, AimTank.CENTER_Y), 3, (255, 255, 255), -1)
        cv2.circle(frame, (AimTank.CENTER_X, AimTank.CENTER_Y), 10, (255, 255, 255), 1)

        # 7. Отображение FPS и информации
        fps_text = f"FPS: {1000 / (cv2.getTickCount() / (cv2.getTickFrequency() + 0.001)):.1f}"
        cv2.putText(frame, fps_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # 8. Показать окно
        cv2.imshow("Tanks Blitz Aimbot", frame)

        # 9. Выход по 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.destroyAllWindows()
print("\n👋 Aimbot stopped.")