from ultralytics import YOLO

# 1. Load the TRUE NANO segmentation model (3.2M parameters, perfect for CPU)
model = YOLO(r'C:\Users\AlexAD\Desktop\AI_vision\local-yolo-models\yolov8m-seg.pt')

# 2. Train with CPU-optimized, small-dataset settings
results = model.train(
    data=r'C:\Users\AlexAD\Desktop\AI_vision\arrow\data.yaml',
    epochs=50,
    imgsz=224,  # Fixed: 224 is a multiple of 32 (optimal for YOLO stride)
    batch=4,  # Reduced to 4 for faster CPU iteration with the Nano model
    device='cpu',
    workers=2,
    patience=15,  # Reduced patience. Tiny datasets overfit fast; stop early.
    name='arrow_cpu_run',

    # --- CRITICAL FIXES FOR TINY DATASETS ---
    freeze=10,  # Freezes the first 10 layers (the backbone).
    # Prevents the model from destroying pre-trained features.
    lr0=0.001,  # Lower initial learning rate for stable, smooth updates.
    mosaic=0.0,  # DISABLED: Mosaic blends 4 images. On 7 images, this creates
    # useless artifacts and confuses the model.
    mixup=0.0,  # DISABLED: Mixup blends two images. Same reason as above.
    copy_paste=0.0  # DISABLED: Prevents copying masks that might overlap incorrectly
    # on a tiny dataset.
)