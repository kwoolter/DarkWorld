import darkworld.model as model
import darkworld.view as view

import os
import pygame
import sys
import numpy as np
from pygame.locals import *


class DWController:

    def __init__(self):
        print("init")

        self.m = model.DWModel("Dark World")
        self.v = view.DWMainFrame(self.m)

    def initialise(self):

        pygame.init()

        self.m.initialise()
        self.v.initialise()

    def end(self):
        self.m.end()
        self.v.end()

    def run(self):

        print("running")

        self.m.print()
        self.v.print()

        self.move_speed = 2

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        FPSCLOCK = pygame.time.Clock()

        pygame.time.set_timer(USEREVENT + 1, 20)
        pygame.time.set_timer(USEREVENT + 2, 300)
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, USEREVENT])

        loop = True

        while loop is True:

            # Loop to process game events
            event = self.m.get_next_event()

            while event is not None:

                try:

                    self.m.process_event(event)
                    self.v.process_event(event)

                    print(str(event))

                except Exception as err:
                    print(str(err))

                if event.type == model.Event.QUIT:
                    loop = False

                event = self.m.get_next_event()

            # Loop to process pygame events
            for event in pygame.event.get():

                # Timer events
                if event.type == USEREVENT + 1:

                    try:

                        self.m.tick()

                    except Exception as err:
                        print(str(err))

                elif event.type == KEYUP:
                    if event.key == K_SPACE:
                        print("interact")
                        self.m.interact()
                    elif event.key == K_F12:
                        self.v.print()
                        self.m.print()
                    elif event.key == K_F11:
                        self.v.world_view.m2v.infinity += 10
                    elif event.key == K_F10:
                        self.v.world_view.m2v.infinity -= 10
                    elif event.key == K_q:

                        text = self.m.get_conversation("Rosie").get_next_line().text
                        self.v.text_box.model = text

                elif event.type == QUIT:
                    loop = False

                # Timer for Computer AI moves
                elif event.type == USEREVENT + 2:
                    self.v.tick()

            keys = pygame.key.get_pressed()
            if keys[K_LEFT]:

                self.m.move_player(np.array(model.World3D.WEST) * self.move_speed)
            elif keys[K_RIGHT]:

                self.m.move_player(np.array(model.World3D.EAST) * self.move_speed)

            if keys[K_UP]:

                self.m.move_player(np.array(model.World3D.DOWN) * self.move_speed)
            elif keys[K_DOWN]:

                self.m.move_player(np.array(model.World3D.UP) * self.move_speed)

            # if keys[K_q]:
            #
            #     self.m.move_player(np.array(model.World3D.NORTH) * 1)
            # elif keys[K_e]:
            #
            #     self.m.move_player(np.array(model.World3D.SOUTH) * 1)

            self.v.draw()
            self.v.update()

            FPSCLOCK.tick(50)

        self.end()
