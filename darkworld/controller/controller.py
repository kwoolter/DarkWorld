import darkworld.model as model
import darkworld.view as view
import darkworld.audio as audio

import os
import pygame
import sys
import numpy as np
from pygame.locals import *


class DWController:

    def __init__(self):
        self.m = model.DWModel("Dark World")
        self.v = view.DWMainFrame(self.m)
        self.audio = audio.AudioManager()

    def initialise(self):

        pygame.init()

        self.m.initialise()
        self.v.initialise()
        self.audio.initialise()

    def end(self):
        self.m.end()
        self.v.end()
        self.audio.end()

    def run(self):

        self.move_speed = 2

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        FPSCLOCK = pygame.time.Clock()

        pygame.time.set_timer(USEREVENT + 1, 20)
        pygame.time.set_timer(USEREVENT + 2, 300)
        pygame.time.set_timer(USEREVENT + 3, 8000)
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, USEREVENT])

        loop = True

        while loop is True:

            # Loop to process game events
            event = self.m.get_next_event()
            while event is not None:

                try:
                    self.m.process_event(event)
                    self.v.process_event(event)
                    self.audio.process_event(event)

                except Exception as err:
                    print(str(err))

                if event.type == model.Event.QUIT:
                    loop = False

                event = self.m.get_next_event()

            # Loop to process pygame events
            for event in pygame.event.get():

                if self.m.state == model.DWModel.STATE_PLAYING:

                    # Timer events
                    if event.type == USEREVENT + 1:

                        self.m.tick()

                        # try:
                        #     self.m.tick()
                        # except Exception as err:
                        #     print(str(err))

                    # Timer for Computer AI moves
                    elif event.type == USEREVENT + 2:
                        self.v.tick()

                    # Key events
                    elif event.type == KEYUP:

                        if event.key == K_SPACE:
                            self.m.interact()
                        elif event.key == K_i:
                            self.v.inventory_show()
                        elif event.key == K_ESCAPE:
                            self.m.pause()
                        elif event.key == K_F12:
                            self.v.print()
                            self.m.print()
                            self.audio.print()
                        elif event.key == K_F1:
                            self.m.help()
                        elif event.key == K_F2:
                            self.audio.change_volume()
                        elif event.key == K_F3:
                            self.audio.change_volume(-0.1)
                        elif event.key == K_F4:
                            self.m.move_world()
                        elif event.key == K_F11:
                            self.v.world_view.m2v.infinity += 10
                        elif event.key == K_F10:
                            self.v.world_view.m2v.infinity -= 10
                        # elif event.key == K_PAGEUP:
                        #     self.v.world_view.object_size_scale += 0.01
                        # elif event.key == K_PAGEDOWN:
                        #     self.v.world_view.object_size_scale -= 0.01

                    keys = pygame.key.get_pressed()
                    if keys[K_LEFT] or keys[K_a]:
                        self.m.move_player(np.array(model.World3D.WEST) * self.move_speed)
                    elif keys[K_RIGHT] or keys[K_d]:
                        self.m.move_player(np.array(model.World3D.EAST) * self.move_speed)
                    if keys[K_UP] or keys[K_w]:
                        self.m.move_player(np.array(model.World3D.DOWN) * self.move_speed)
                    elif keys[K_DOWN] or keys[K_s]:
                        self.m.move_player(np.array(model.World3D.UP) * self.move_speed)
                    elif keys[K_PAGEUP]:
                        self.v.world_view.zoom_view(0.01)
                    elif keys[K_PAGEDOWN]:
                        self.v.world_view.zoom_view(-0.01)
                    elif keys[K_PAGEUP]:
                        self.v.world_view.zoom_view(0.01)
                    elif keys[K_HOME]:
                        self.v.world_view.zoom_view()

                # Process events for when the game is in state READY
                elif self.m.state == model.DWModel.STATE_READY:

                    # Key events
                    if event.type == KEYUP:
                        # Space to start the game
                        if event.key == K_SPACE:
                            self.m.start()
                        elif event.key == K_F2:
                            self.audio.change_volume()
                        elif event.key == K_F3:
                            self.audio.change_volume(-0.1)
                    # Timer events
                    elif event.type == USEREVENT + 2:
                        self.v.tick()

                    # Timer for talking
                    elif event.type == USEREVENT + 3:
                        self.m.talk_to_npc(npc_object=None, npc_name="The Master", world_id=self.m.state)

                # Process events for when the game is in state PAUSED
                elif self.m.state == model.DWModel.STATE_PAUSED:

                    # Key events
                    if event.type == KEYUP:
                        # Space to unpause the game
                        if event.key == K_SPACE:
                            self.m.pause()
                        elif event.key == K_F2:
                            self.audio.change_volume()
                        elif event.key == K_F3:
                            self.audio.change_volume(-0.1)
                        elif event.key == K_F12:
                            print("\n\nG A M E   S T A T E")
                            self.v.print()
                            self.m.print()
                            self.audio.print()
                        elif event.key == K_q:
                            self.m.player_died()

                    # Timer events
                    elif event.type == USEREVENT + 2:
                        self.v.tick()

                    # Timer for talking
                    elif event.type == USEREVENT + 3:
                        self.m.talk_to_npc(npc_object=None, npc_name="The Master", world_id=self.m.state)

                # Process events for when the game is in state GAME_OVER
                elif self.m.state == model.DWModel.STATE_GAME_OVER:

                    # Key events
                    if event.type == KEYUP:
                        # Space to restart the game
                        if event.key == K_SPACE:
                            self.m.initialise()

                    # Timer events
                    elif event.type == USEREVENT + 2:
                        self.v.tick()

                # Quit event
                if event.type == QUIT:
                    loop = False

            self.v.draw()
            self.v.update()

            FPSCLOCK.tick(60)

        self.end()
