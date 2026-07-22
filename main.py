import cv2
import time


from camera import Camera
from hand_tracker import HandTracker
from hologram import Hologram
from renderer import Renderer


from config import WINDOW_NAME



def main():


    camera = Camera()

    tracker = HandTracker()

    hologram = Hologram()

    renderer = Renderer()



    cv2.namedWindow(
        WINDOW_NAME,
        cv2.WINDOW_NORMAL
    )


    cv2.setWindowProperty(
        WINDOW_NAME,
        cv2.WND_PROP_FULLSCREEN,
        cv2.WINDOW_FULLSCREEN
    )



    while True:


        frame = camera.read()


        if frame is None:
            break



        hand = tracker.track(
            frame
        )


        hologram.update(
            hand
        )


        frame = hologram.draw(
            frame
        )


        frame = renderer.draw(
            frame
        )



        cv2.imshow(
            WINDOW_NAME,
            frame
        )



        key = cv2.waitKey(1)


        if key == 27:
            break



    camera.release()

    cv2.destroyAllWindows()




if __name__ == "__main__":

    main()