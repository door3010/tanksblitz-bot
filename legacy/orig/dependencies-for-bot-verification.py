import sys
import numpy as np
import cv2
import gymnasium as gym
import stable_baselines3 as sb3
from ultralytics import YOLO
import mss
import torch

print(f"Python: {sys.version.split()[0]}")
print(f"Numpy: {np.__version__} (Must be 1.x.x)")
print(f"OpenCV: {cv2.__version__} (Must be 4.10.0)")
print(f"Gymnasium: {gym.__version__}")
print(f"Stable Baselines3: {sb3.__version__}")
print(f"PyTorch CUDA Available: {torch.cuda.is_available()}")
print("\n✅ All dependencies loaded successfully!")