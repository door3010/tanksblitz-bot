import numpy as np
from collections import deque
from PIL import Image

im = Image.open('true-bw-minimap.png').convert('L')
w, h = im.size
binary = im.point(lambda p: p > 128 and 1)
binary = binary.resize((w,h),Image.NEAREST)
w, h = binary.size

maze = np.array(binary)
print(len(maze))

# Convert the numpy array into a multi-line string
maze_str = "\n".join("".join(str(cell) for cell in row) for row in maze)

# Write it to config.py
with open("config_minimap.py", "w") as f:
    f.write("MAZE_STR = \"\"\"\n")
    f.write(maze_str)
    f.write("\n\"\"\"\n")