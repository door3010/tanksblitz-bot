import cv2
import numpy as np
import mss

class ScreenGrabber:
    def __init__(self, monitor):
        self.monitor=monitor
        self.sct = mss.mss()
        self.ScreenGrabbing = True

    def start_grabbing(self):
        sct_img = self.sct.grab(self.monitor)
        frame = np.array(sct_img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame

    def stop(self):
        self.ScreenGrabbing=False
        cv2.destroyAllWindows()

    cv2.destroyAllWindows()
