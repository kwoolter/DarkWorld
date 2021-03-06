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
        self._debug = False

    def initialise(self):

        pygame.init()

        self.m.initialise()
        self.v.initialise()
        self.audio.initialise()

    def debug(self):
        self._debug = not self._debug
        self.m.events.add_event(model.Event(type=model.Event.DEBUG,
                                    name="Debug={0}".format(self._debug),
                                    description="Debug mode = {0}".format(self._debug)))
        if self._debug is True:
            print("\n\nDEBUG MODE\n\n")

    def end(self):
        self.m.end()
        self.v.end()
        self.audio.end()

    def run(self):

        self.move_speed = 2

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        FPSCLOCK = pygame.time.Clock()

        # Model tick timer
        pygame.time.set_timer(USEREVENT + 1, 15)

        # View tick timer
        pygame.time.set_timer(USEREVENT + 2, 300)

        # Sound effects tick timer
        pygame.time.set_timer(USEREVENT + 3, 8000)

        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, USEREVENT])

        loop = True

        while loop is True:

            # Loop to process Dark World game events
            event = self.m.get_next_event()
            while event is not None:

                try:
                    self.m.process_event(event)
                    self.v.process_event(event)

                    if event.name == model.Event.NEW_WORLD:
                        print("Changing world skin = {0}".format(self.m.world.skin))
                        self.audio.current_music_theme = self.m.world.skin
                        self.audio.current_sound_theme = self.m.world.skin
                        self.audio.print()

                    self.audio.process_event(event)

                except Exception as err:
                    print("Caught exception {0}".format(str(err)))

                if event.type == model.Event.QUIT:
                    loop = False
                    break

                event = self.m.get_next_event()

            # If we are playing the game then process all of the key controls
            if self.m.state == model.DWModel.STATE_PLAYING:
                # Key pressed events - more time critical actions
                keys = pygame.key.get_pressed()

                # First key if the movement keys are pressed
                move_vector = model.World3D.DUMMY

                if keys[K_LEFT] or keys[K_a]:
                    move_vector = np.add(move_vector, np.array(model.World3D.WEST))

                elif keys[K_RIGHT] or keys[K_d]:
                    move_vector = np.add(move_vector, np.array(model.World3D.EAST))

                if keys[K_UP] or keys[K_w]:
                    move_vector = np.add(move_vector, np.array(model.World3D.DOWN))

                elif keys[K_DOWN] or keys[K_s]:
                    move_vector = np.add(move_vector, np.array(model.World3D.UP))

                # If the player chose to move then attempt to do so...
                if np.array_equal(move_vector, model.World3D.DUMMY) is False:
                    self.m.move_player(move_vector * self.move_speed)

                # Now see if the player wants to change the camera zoom...
                if keys[K_PAGEUP]:
                    self.v.world_view.zoom_view(0.01)
                elif keys[K_PAGEDOWN]:
                    self.v.world_view.zoom_view(-0.01)
                elif keys[K_HOME]:
                    self.v.world_view.zoom_view()

            # Loop to process pygame events
            for event in pygame.event.get():

                if self.m.state == model.DWModel.STATE_PLAYING:

                    # Timer events for the model to process
                    if event.type == USEREVENT + 1:

                        self.m.tick()

                    # Timer for the view time based events
                    elif event.type == USEREVENT + 2:
                        self.v.tick()

                    # Timer events for audio time-based events
                    elif event.type == USEREVENT + 3:
                        self.audio.get_theme_sound(model.Event.RANDOM_ENVIRONMENT, self.m.world.skin)

                    # Key UP events - less time critical actions
                    elif event.type == KEYUP:

                        if event.key == K_SPACE:
                            self.m.interact()
                        elif event.key == K_i:
                            self.v.inventory_show()
                        elif event.key == K_ESCAPE:
                            self.m.pause()
                        elif event.key == K_F12 and self._debug is True:
                            self.v.print()
                            self.m.print()
                            self.audio.print()
                        elif event.key == K_F1:
                            self.m.help()
                        elif event.key == K_F2:
                            self.audio.change_volume()
                        elif event.key == K_F3:
                            self.audio.change_volume(-0.1)
                        elif event.key == K_F4 and self._debug is True:
                            self.m.move_world()
                        elif event.key == K_F5 and self._debug is True:
                            self.m.reset()
                        elif event.key == K_F11:
                            self.v.world_view.m2v.infinity += 10
                        elif event.key == K_F10:
                            self.v.world_view.m2v.infinity -= 10

                    # Key DOWN events - less time critical actions
                    elif event.type == KEYDOWN:

                        if event.key == K_z:
                            self.m.do_melee_attack()

                # Process events for when the game is in state READY
                elif self.m.state == model.DWModel.STATE_LOADED:

                    # Key events
                    if event.type == KEYUP:
                        # Space to start the game
                        if event.key == K_SPACE:
                            self.m.start()
                            self.audio.current_music_theme = self.m.world.skin
                            self.audio.current_sound_theme = self.m.world.skin
                        elif event.key == K_F2:
                            self.audio.change_volume()
                        elif event.key == K_F3:
                            self.audio.change_volume(-0.1)
                        elif event.key == K_F4:
                            loop = False
                        elif event.key == K_F12 and self._debug is True:
                            self.v.print()
                            self.m.print()
                            self.audio.print()
                    # Timer events
                    elif event.type == USEREVENT + 2:
                        self.v.tick()

                    # Timer for talking
                    elif event.type == USEREVENT + 3:
                        self.m.talk_to_npc(npc_object=None, npc_name="The Master", world_id=self.m.state)

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
                        # Debug print game status info
                        elif event.key == K_F12 and self._debug is True:
                            self.v.print()
                            self.m.print()
                            self.audio.print()
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
                        elif event.key == K_F12 and self._debug is True:
                            print("\n\nG A M E   S T A T E")
                            self.v.print()
                            self.m.print()
                            self.audio.print()
                        elif event.key == K_F11:
                            self.debug()
                        elif event.key == K_q:
                            self.m.player_died()

                    # Timer events
                    elif event.type == USEREVENT + 2:
                        self.v.tick()

                    # Timer for talking
                    elif event.type == USEREVENT + 3:
                        self.m.talk_to_npc(npc_object=None, npc_name="The Master", world_id=self.m.state)

                # Process events for when the game is in state READY
                elif self.m.state == model.DWModel.STATE_WORLD_COMPLETE:
                    # Key events
                    if event.type == KEYUP:
                        # Space to proceed to next world
                        if event.key == K_SPACE:
                            self.m.move_world(do_copy = True)
                            self.m.state = model.DWModel.STATE_PLAYING

                    # Timer events
                    elif event.type == USEREVENT + 2:
                        self.v.tick()

                # Process events for when the game is in state GAME_OVER
                elif self.m.state == model.DWModel.STATE_GAME_OVER:

                    # Key events
                    if event.type == KEYUP:
                        # Space to restart the game
                        if event.key == K_SPACE:
                            self.m.initialise()
                        elif event.key == K_F12 and self._debug is True:
                            print("\n\nG A M E   S T A T E")
                            self.v.print()
                            self.m.print()
                            self.audio.print()

                    # Timer events
                    elif event.type == USEREVENT + 2:
                        self.v.tick()

                    # Timer for talking
                    elif event.type == USEREVENT + 3:
                        self.m.talk_to_npc(npc_object=None, npc_name="The Master", world_id=self.m.state)

                # Quit event
                if event.type == QUIT:
                    loop = False

            self.v.draw()
            self.v.update()

            FPSCLOCK.tick(60)

        self.end()
