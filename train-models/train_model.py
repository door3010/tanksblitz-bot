from ultralytics import YOLO

# 1. Load the NANO segmentation model (Perfect for small datasets & CPU)
model = YOLO(r'C:\Users\AlexAD\Desktop\tanksblitz-bot\yolo-models\yolov8m-seg.pt')

# 2. Train with CPU-optimized, small-dataset settings
results = model.train(
    data=r'C:\Users\AlexAD\Desktop\tanksblitz-bot\datasets\e5\data.yaml',
    epochs=150,         # Give it more epochs since it's a smaller model
    imgsz=416,          # 416 is much faster on CPU than 640, and plenty for small objects
    batch=8,            # Keep batch size manageable for CPU RAM
    device='cpu',       # Force CPU
    workers=2,          # Prevents CPU from freezing your computer
    patience=30,        # Stop training early if it stops improving for 30 epochs
    name='e5_cpu_run'  # Name of your output folder
)