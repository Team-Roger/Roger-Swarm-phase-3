import cv2
import numpy as np
import math
import random


from config import (
    HOLOGRAM_RADIUS,
    INNER_RADIUS,
    PARTICLE_COUNT,
    ROTATION_SPEED,
    SMOOTHING,

    ICE_BLUE,
    WHITE,
    GLOW,

    OUTER_PURPLE,
    INNER_SHELL,

    STAR_WHITE,
    CORE_BLUE,
    STAR,
    AURA
)


class Hologram:


    def __init__(self):

        self.x = 320
        self.y = 240

        self.alpha = 0

        self.rotation = 0

        self.wave = 0


        self.particles = []


        for i in range(PARTICLE_COUNT):

            self.particles.append({

                "angle":
                random.uniform(
                    0,
                    math.pi*2
                ),

                "radius":
                random.randint(
                    60,
                    115
                ),

                "speed":
                random.uniform(
                    0.01,
                    0.035
                )

            })



    # ==========================
    # Hand position
    # ==========================

    def back_hand_position(self, hand):

        return (

            hand["palm_x"],

            hand["palm_y"] + 30

        )



    def open_palm_position(self, hand):

        return (

            hand["palm_x"],

            hand["palm_y"] - 65

        )



    # ==========================
    # Update
    # ==========================

    def update(self, hand):


        if hand and hand["open"]:


            if hand["mode"] == "open":

                tx, ty = (
                    self.open_palm_position(hand)
                )


            else:

                tx, ty = (
                    self.back_hand_position(hand)
                )



            self.x = (

                self.x * SMOOTHING

                +

                tx * (1-SMOOTHING)

            )


            self.y = (

                self.y * SMOOTHING

                +

                ty * (1-SMOOTHING)

            )


            self.alpha = min(

                1,

                self.alpha + 0.05

            )


        else:


            self.alpha -= 0.04


            if self.alpha < 0:

                self.alpha = 0



        self.rotation += ROTATION_SPEED

        self.wave += 0.05




    # ==========================
    # Glow
    # ==========================

    def draw_glow(self, frame, center):


        glow = np.zeros_like(frame)


        pulse = int(

            8 * math.sin(self.wave)

        )


        cv2.circle(

            glow,

            center,

            HOLOGRAM_RADIUS + 35 + pulse,

            GLOW,

            8

        )


        glow = cv2.GaussianBlur(

            glow,

            (41,41),

            0

        )


        frame = cv2.addWeighted(

            frame,

            1,

            glow,

            0.25*self.alpha,

            0

        )


        return frame




    # ==========================
    # Glass Shell
    # ==========================

       # ==========================
    # Glass Shell
    # ==========================

    def draw_glass_shell(
          self,
          overlay,
          center):


        # dark galaxy transparent core
        cv2.circle(
            overlay,
            center,
            HOLOGRAM_RADIUS,
            CORE_BLUE,
            -1
        )


        # ==========================
        # Purple outer glass shells
        # ==========================

        cv2.circle(
            overlay,
            center,
            HOLOGRAM_RADIUS,
            OUTER_PURPLE,
            4
        )


        # second purple energy shell

        cv2.circle(
            overlay,
            center,
            HOLOGRAM_RADIUS + 8,
            OUTER_PURPLE,
            2
        )


        # third purple outer aura shell

        cv2.circle(
            overlay,
            center,
            HOLOGRAM_RADIUS + 16,
            OUTER_PURPLE,
            1
        )


        # ==========================
        # Light green inner shell
        # ==========================

        cv2.circle(
            overlay,
            center,
            HOLOGRAM_RADIUS - 12,
            INNER_SHELL,
            2
        )


    # ==========================
    # Energy Rings
    # ==========================

    def draw_energy_rings(
            self,
            overlay,
            center):


        rot = math.degrees(

            self.rotation

        )


        for i in range(12):


            start = (

                rot

                +

                i*35

            )


            end = start + 15



            if i % 2 == 0:

                color = OUTER_PURPLE

            else:

                color = ICE_BLUE



            cv2.ellipse(

                overlay,

                center,

                (

                    HOLOGRAM_RADIUS+15,

                    HOLOGRAM_RADIUS+15

                ),

                0,

                start,

                end,

                color,

                2

            )



        # middle ring


        cv2.ellipse(

            overlay,

            center,

            (

                INNER_RADIUS+25,

                INNER_RADIUS+25

            ),

            0,

            -rot,

            -rot+120,

            INNER_SHELL,

            2

        )



        # inner scanner


        cv2.circle(

            overlay,

            center,

            INNER_RADIUS,

            INNER_SHELL,

            2

        )




    # ==========================
    # Energy Waves
    # ==========================

    def draw_waves(
            self,
            overlay,
            center):


        for i in range(3):


            radius = (

                INNER_RADIUS

                +

                35

                +

                int(

                    (self.wave*20+i*20)

                    %

                    60

                )

            )


            cv2.circle(

                overlay,

                center,

                radius,

                INNER_SHELL,

                1

            )




    # ==========================
    # Core
    # ==========================

    def draw_core(
            self,
            overlay,
            center):


        cv2.circle(

            overlay,

            center,

            10,

            STAR_WHITE,

            -1

        )


        cv2.circle(

            overlay,

            center,

            20,

            ICE_BLUE,

            2

        )


        cv2.circle(

            overlay,

            center,

            32,

            INNER_SHELL,

            1

        )




    # ==========================
    # Particles
    # ==========================

    def draw_particles(
            self,
            overlay):


        colors = [

          OUTER_PURPLE,

          INNER_SHELL,

          STAR,

          ICE_BLUE

        ]



        for i, p in enumerate(self.particles):


            p["angle"] += p["speed"]



            x = (

                self.x

                +

                math.cos(

                    p["angle"]

                )

                *

                p["radius"]

            )



            y = (

                self.y

                +

                math.sin(

                    p["angle"]

                )

                *

                p["radius"]

            )



            cv2.circle(

                overlay,

                (

                    int(x),

                    int(y)

                ),

                2,

                colors[i % len(colors)],

                -1

            )




    # ==========================
    # Main Draw
    # ==========================

    def draw(self, frame):


        if self.alpha <= 0:

            return frame



        center = (

            int(self.x),

            int(self.y)

        )



        frame = self.draw_glow(

            frame,

            center

        )


        overlay = frame.copy()



        self.draw_glass_shell(

            overlay,

            center

        )


        self.draw_waves(

            overlay,

            center

        )


        self.draw_energy_rings(

            overlay,

            center

        )


        self.draw_particles(

            overlay

        )


        self.draw_core(

            overlay,

            center

        )



        frame = cv2.addWeighted(

            overlay,

            self.alpha,

            frame,

            1-self.alpha,

            0

        )


        return frame