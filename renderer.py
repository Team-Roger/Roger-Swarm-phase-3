import cv2
import numpy as np

from config import TITLE, CYAN, BLUE, PURPLE



class Renderer:


    def __init__(self):

        self.font = cv2.FONT_HERSHEY_SIMPLEX



    def draw(self, frame):


        h, w, _ = frame.shape



        overlay = frame.copy()



        # --------------------------------
        # Top left HUD background
        # --------------------------------


        cv2.rectangle(

            overlay,

            (15,15),

            (260,80),

            (0,0,0),

            -1

        )



        frame = cv2.addWeighted(

            overlay,

            0.35,

            frame,

            0.65,

            0

        )



        # --------------------------------
        # Text glow
        # --------------------------------


        position = (
            30,
            48
        )


        glow = np.zeros_like(frame)



        cv2.putText(

            glow,

            TITLE,

            position,

            self.font,

            0.9,

            CYAN,

            3,

            cv2.LINE_AA

        )



        glow = cv2.GaussianBlur(

            glow,

            (15,15),

            0

        )



        frame = cv2.addWeighted(

            frame,

            1,

            glow,

            0.35,

            0

        )




        # --------------------------------
        # Main title
        # --------------------------------


        cv2.putText(

            frame,

            TITLE,

            position,

            self.font,

            0.9,

            CYAN,

            2,

            cv2.LINE_AA

        )



        # --------------------------------
        # Subtitle line
        # --------------------------------


        cv2.line(

            frame,

            (30,60),

            (220,60),

            PURPLE,

            2

        )



        # small corner HUD mark

        cv2.line(

            frame,

            (15,15),

            (35,15),

            BLUE,

            2

        )


        cv2.line(

            frame,

            (15,15),

            (15,35),

            BLUE,

            2

        )



        return frame