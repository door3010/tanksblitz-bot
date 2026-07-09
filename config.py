class AimTank:
    mle_model_path = r"runs/segment/mle_cpu_run/weights/best.pt"
    monitor = {
        "top": 0,
        "left": 0,
        "width": 800,
        "height": 600
    }
    CENTER_X = monitor["width"] // 2
    CENTER_Y = monitor["height"] // 2
    SMOOTHING = 0.15  # Коэффициент сглаживания (0.1-0.3)
    AIM_HEIGHT_CORR = -0.1  # Поправка на высоту (-0.2 = выше, +0.2 = ниже)
    SHOOT_DIST = 50  # Дистанция для авто-выстрела (пикселей от центра)
    AUTO_SHOOT = True  # Включить авто-стрельбу
    CONFIDENCE_THRESHOLD = 0.5
    IOU_THRESHOLD = 0.45

class Minimap:
    arrow_model_path = r'C:\Users\AlexAD\Desktop\AI_vision\runs\segment\arrow_cpu_run-2\weights\best.pt'

    monitor = {
        "top": 0,
        "left": 400,
        "width": 215,
        "height": 215
    }
