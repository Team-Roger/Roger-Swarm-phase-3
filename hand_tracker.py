import cv2
import mediapipe as mp


from config import (
    MAX_HANDS,
    DETECTION_CONFIDENCE,
    TRACKING_CONFIDENCE
)



class HandTracker:


    def __init__(self):

        self.mp_hands = mp.solutions.hands


        self.hands = self.mp_hands.Hands(

            max_num_hands=MAX_HANDS,

            min_detection_confidence=
            DETECTION_CONFIDENCE,

            min_tracking_confidence=
            TRACKING_CONFIDENCE
        )

    def is_hand_open(self, hand):


        fingers = []


        # index finger
        fingers.append(
            hand.landmark[8].y <
            hand.landmark[6].y
        )


        # middle finger
        fingers.append(
            hand.landmark[12].y <
            hand.landmark[10].y
        )


        # ring finger
        fingers.append(
            hand.landmark[16].y <
            hand.landmark[14].y
        )


        # pinky
        fingers.append(
            hand.landmark[20].y <
            hand.landmark[18].y
        )


        # count open fingers

        open_count = sum(fingers)


        # only need 2 fingers open
        # to activate hologram

        if open_count >= 2:

            return True


        return False

    def track(self, frame):


        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )


        result = self.hands.process(rgb)



        if result.multi_hand_landmarks:


            hand = result.multi_hand_landmarks[0]


            h,w,_ = frame.shape



            # wrist

            wrist_x = int(
                hand.landmark[0].x*w
            )

            wrist_y = int(
                hand.landmark[0].y*h
            )



            # palm center

            palm_x = int(
                hand.landmark[9].x*w
            )

            palm_y = int(
                hand.landmark[9].y*h
            )



            # palm orientation

            wrist = hand.landmark[0]
            middle = hand.landmark[9]


            if middle.y < wrist.y:

                  palm_mode = "open"


            else:

                palm_mode = "back"



            return {

              "wrist_x": wrist_x,

              "wrist_y": wrist_y,

              "palm_x": palm_x,

              "palm_y": palm_y,

              "mode": palm_mode,

              "open": self.is_hand_open(hand)

            }


        return None