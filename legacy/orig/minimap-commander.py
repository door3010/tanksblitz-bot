import tkinter as tk
class Paint():
    def __init__(self):
        self.window = tk.Tk()
        self.sizex = 200
        self.sizey = 200
        self.canvas = tk.Canvas(self.window, width=self.sizex,height=self.sizey, highlightthickness=0)
        self.canvas.config(bg="thistle")
        self.canvas.pack()
        self.img = tk.PhotoImage(file=r"C:\Users\AlexAD\Desktop\tanksblitz-bot\images-for-dataset\minimap-player\screenshot_20260708_165952_1.png")
        self.canvas.create_image((0,0), image=self.img, state="normal",anchor='nw')
        self.canvas.bind("<Button-1>",self.color_in)
    def color_in(self, event):
        x, y = event.x, event.y
        print(x,y)
        # paint.window.destroy()
paint = Paint()
paint.window.mainloop()
