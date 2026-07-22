import cv2

from config import CAMERA_WIDTH, CAMERA_HEIGHT


class Camera:

    def __init__(self):

        self.cap = cv2.VideoCapture(0)

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            CAMERA_WIDTH
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            CAMERA_HEIGHT
        )


    def read(self):

        success, frame = self.cap.read()

        if not success:
            return None


        # mirror view
        frame = cv2.flip(frame, 1)

        return frame



    def release(self):

        self.cap.release()