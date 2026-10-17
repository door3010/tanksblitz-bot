import os
import time
from datetime import datetime
import mss
from PIL import Image

# Создаем папку для скриншотов
screenshot_folder = "images-for-dataset/minimap-player"
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)

# Координаты области скриншота
minimap_screenshot_monitor = {
    "left": 0,
    "top": 350,
    "width": 200,
    "height": 200
}

try:
    screenshot_count = 0
    with mss.mss() as sct:
        while True:
            # Делаем скриншот указанной области
            screenshot = sct.grab(minimap_screenshot_monitor)

            # Конвертируем в PIL Image
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

            # Генерируем имя файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(screenshot_folder, f"screenshot_{timestamp}_{screenshot_count}.png")

            # Сохраняем
            img.save(filename)
            screenshot_count += 1

            print(f"Скриншот сохранен: {filename}")

            # Ждем 3 секунды
            time.sleep(3)

except KeyboardInterrupt:
    print("\nПрограмма остановлена")
    print(f"Всего сделано скриншотов: {screenshot_count}")