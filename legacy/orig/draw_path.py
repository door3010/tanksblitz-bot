from PIL import Image
def draw_path(source):
    image = Image.open(r'C:\Users\AlexAD\Desktop\tanksblitz-bot\true-bw-minimap.png')
    for x in range(len(source)):
        image.putpixel((source[x][1],source[x][0]), (0, 255, 0, 255))
    image.save("bw-minimap-with-path.png")