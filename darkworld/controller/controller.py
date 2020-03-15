import darkworld.model as model
import darkworld.view as view

import os
import pygame
import sys
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

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        FPSCLOCK = pygame.time.Clock()

        pygame.time.set_timer(USEREVENT + 1, 150)
        pygame.time.set_timer(USEREVENT + 2, 500)
        pygame.event.set_allowed([QUIT, KEYDOWN, USEREVENT])

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

                event = self.game.get_next_event()

            # Loop to process pygame events
            for event in pygame.event.get():

                # Timer events
                if event.type == USEREVENT + 1:

                    try:

                        self.m.tick()
                        self.v.tick()

                    except Exception as err:
                        print(str(err))

                elif event.type == QUIT:
                    loop = False

                # Timer for Computer AI moves
                elif event.type == USEREVENT + 2:
                    pass

            self.v.draw()
            self.v.update()

            FPSCLOCK.tick(50)

        self.end()

