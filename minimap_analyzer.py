"""Minimap navigation: detect the player arrow, plan a path, drive the tank.

Usage:
    python minimap_analyzer.py

Press 'q' in the OpenCV window to quit.
"""
import cv2

from tanksbot.config import MINIMAP
from tanksbot.detection import load_model
from tanksbot.keyboard import execute_path
from tanksbot.pathing import shortest_path
from tanksbot.screen import ScreenGrabber, position_game_window
from tanksbot.visualize import draw_path


def main() -> None:
    cfg = MINIMAP

    position_game_window(
        cfg.game_window_title,
        cfg.game_window_width,
        cfg.game_window_height,
        cfg.game_window_x,
        cfg.game_window_y,
    )

    model = load_model(cfg.arrow_model_path)
    grabber = ScreenGrabber(cfg.monitor)

    destination = list(cfg.default_destination)  # [row, col]; row -> None after use
    facing = "UP"

    print("Starting detection... Press 'q' in the OpenCV window to quit.")

    while True:
        frame = grabber.grab()
        results = model(frame, conf=cfg.confidence, verbose=False)

        for box in results[0].boxes:
            # Oriented bounding box of the player arrow (4 corner points).
            x1, y1, x2, y2, x3, y3, x4, y4 = box.xyxyxyxy[0].tolist()

            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.line(frame, (int(x1), int(y1)), (int(x3), int(y3)), (0, 255, 0), 2)
            cv2.line(frame, (int(x2), int(y2)), (int(x4), int(y4)), (0, 255, 0), 2)
            cv2.line(frame, (int(x3), int(y3)), (int(x4), int(y4)), (0, 255, 0), 2)

            player_pos_x = (int(x1) + int(x2)) / 2
            player_pos_y = (int(y1) + int(y2)) / 2

            if destination[0] is None:
                continue

            # Pathfinding works in (row, col) == (y, x) coordinates.
            path = shortest_path([int(player_pos_y), int(player_pos_x)], destination)
            if not path:
                print("No path to destination.")
                destination[0] = None
                continue

            print(path)
            facing, _ = execute_path(path, initial_direction=facing, dry_run=False)
            draw_path(path)
            destination[0] = None

        cv2.imshow("Minimap Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
