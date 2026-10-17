"""Click an image in a Tk window to print pixel coordinates.

Usage:
    python tools/pick_coordinates.py [image_path]

Useful for picking navigation targets on the minimap.
"""
import sys
import tkinter as tk

from tanksbot.config import PROJECT_ROOT

DEFAULT_IMAGE = PROJECT_ROOT / "images-for-dataset" / "minimap-player" / "screenshot_20260708_165952_1.png"


class ImagePicker:
    """Tk window showing an image; clicking prints (x, y)."""

    def __init__(self, image_path: str):
        self.window = tk.Tk()
        self.window.title("Coordinate picker")

        self.canvas = tk.Canvas(self.window, highlightthickness=0, bg="thistle")
        self.canvas.pack()

        self.image = tk.PhotoImage(file=image_path)
        self.canvas.create_image((0, 0), image=self.image, state="normal", anchor="nw")
        self.canvas.bind("<Button-1>", self.on_click)

    def on_click(self, event) -> None:
        print(event.x, event.y)

    def run(self) -> None:
        self.window.mainloop()


def main() -> None:
    image_path = sys.argv[1] if len(sys.argv) > 1 else str(DEFAULT_IMAGE)
    ImagePicker(image_path).run()


if __name__ == "__main__":
    main()
