import darkworld.model as model
from .graphics import *
import pygame
import os
import numpy as np
import math
import logging
from darkworld.model.events import *
from collections import deque


class ImageManager:
    DEFAULT_SKIN = "default"
    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    image_cache = {}
    skins = {}
    sprite_sheets = {}
    initialised = False

    def __init__(self):
        pass

    def initialise(self):
        if ImageManager.initialised is False:
            self.load_skins()
            self.load_sprite_sheets()

    def get_image(self, image_file_name: str, width: int = 32, height: int = 32):

        transparent = pygame.Color(255, 22, 33)

        if image_file_name not in ImageManager.image_cache.keys():

            if image_file_name in self.sprite_sheets.keys():
                file_name, rect = self.sprite_sheets[image_file_name]
                filename = ImageManager.RESOURCES_DIR + file_name
                logging.info("Loading image {0} from {1} at {2}...".format(image_file_name, filename, rect))

                image_sheet = spritesheet(filename)
                original_image = image_sheet.image_at(rect)
            else:
                filename = ImageManager.RESOURCES_DIR + image_file_name
                logging.info("Loading image {0}...".format(filename))
                image_sheet = spritesheet(filename)
                original_image = image_sheet.image_at()

            try:

                image = pygame.transform.scale(original_image, (width, height))
                smallest_size = image.get_bounding_rect()
                print(f'{image_file_name}:{image.get_rect()} smallest={smallest_size}')
                cropped_image = pygame.Surface((smallest_size.width, smallest_size.height))
                cropped_image.fill(transparent)
                cropped_image.blit(image, dest=(0,0), area= smallest_size)
                cropped_image.set_colorkey(transparent)
                #ImageManager.image_cache[image_file_name] = cropped_image
                ImageManager.image_cache[image_file_name] = original_image
                logging.info("Image {0} loaded and scaled to {1}x{2} and cached.".format(filename, width, height))


            except Exception as err:
                print(str(err))

        return self.image_cache[image_file_name]

    def load_skins(self):

        new_skin_name = ImageManager.DEFAULT_SKIN
        new_skin = (new_skin_name, {

            model.Objects.EMPTY: None,

            model.Objects.FAKE_WALL: "wall.png",
            model.Objects.BOOK: "rpg_sprite_gold2-5.png",
            model.Objects.COINS: "rpg_sprite_gold1-12.png",
            model.Objects.SCROLL: "rpg_sprite_gold0-5.png",
            model.Objects.ENEMY1: "rpg_sprite_bw5-15.png",
            model.Objects.ENEMY2: "rpg_sprite_bw6-15.png",
            model.Objects.EXTRA_LIFE: "rpg_sprite_gold1-14.png",
            model.Objects.BLOCK1: "block1.png",
            model.Objects.BLOCK2: "block2.png",
            model.Objects.DOOR1: "door.png",
            model.Objects.DOOR1_OPEN: "door_open.png",
            model.Objects.DOOR2: "door.png",
            model.Objects.DOOR2_OPEN: "door_open.png",
            # model.Objects.PLAYER: ("robotA0000.png", "robotA0001.png", "robotA0002.png", "robotA0003.png"),
            model.Objects.PLAYER: ("knight_bw0.png", "knight_bw1.png", "knight_bw2.png", "knight_bw3.png"),
            model.Objects.PLAYER2: ("knight_bw4.png", "knight_bw5.png", "knight_bw6.png", "knight_bw7.png"),
            model.Objects.HELMET1: "rpg_sprite_gold2-10.png",
            model.Objects.HELMET2: "rpg_sprite_gold3-10.png",
            model.Objects.MAP: "rpg_sprite_gold1-5.png",
            model.Objects.MONSTER1: "bear.png",
            model.Objects.MONSTER2: "winter_tiles0.png",
            model.Objects.NPC1: "rpg_sprite_bw0-15.png",
            model.Objects.NPC2: "rpg_sprite_bw1-15.png",
            model.Objects.BIG_MONSTER1: "bear.png",
            model.Objects.BIG_MONSTER2: "winter_tiles0.png",
            model.Objects.BOMB: "rpg_sprite_gold2-8.png",
            # model.Objects.PLAYER: ("man0.png", "man2.png", "man1.png", "man2.png"),
            # model.Objects.TREASURE: "treasure.png",
            model.Objects.TREASURE: ("token0.png", "token1.png", "token2.png", "token3.png"),
            model.Objects.TREASURE_CHEST: "rpg_sprite_gold2-3.png",
            model.Objects.DECOR1: "rpg_sprite_gold0-13.png",
            model.Objects.DECOR2: "rpg_sprite_gold1-13.png",
            model.Objects.TRAP: ("trap0.png", "trap1.png", "trap2.png", "trap3.png",
                                 "trap4.png", "trap5.png", "trap6.png", "trap7.png",
                                 "trap6.png", "trap5.png", "trap4.png", "trap3.png",
                                 "trap2.png", "trap1.png", "trap0.png", "trap0.png"),
            model.Objects.TRAP_DISABLE: "trap_disable.png",
            model.Objects.KEY: "key2.png",
            model.Objects.BOSS_KEY: "key4.png",
            model.Objects.TILE1: "tile1.png",
            model.Objects.TILE2: "tile2.png",
            model.Objects.TILE3: "tile3.png",
            model.Objects.TILE4: "tile4.png",
            model.Objects.TELEPORT: ("teleport_00.png", "teleport_01.png", "teleport_02.png"),
            model.Objects.HOLE: "hole.png",
            model.Objects.EXIT_NEXT: "exit_green2.png",
            model.Objects.EXIT_PREVIOUS: "exit_red.png",
            model.Objects.POTION1: "rpg_sprite_gold5-4.png",
            model.Objects.POTION2: "rpg_sprite_gold4-4.png",
            model.Objects.SIGN_1: "rpg_sprite_gold3-14.png",
            model.Objects.SIGN_2: "rpg_sprite_gold3-14.png",
            model.Objects.SWITCH_TILE1: None,
            model.Objects.SWITCH_TILE2: None,
            model.Objects.SWITCH_TILE3: None,
            model.Objects.SWITCH_TILE4: None,
            model.Objects.SWITCH_1: ("switch7.png", "switch6.png"),
            model.Objects.SWITCH_2: ("switch7.png", "switch6.png"),
            model.Objects.SWITCH_3: ("switch7.png", "switch6.png"),
            model.Objects.SWITCH_4: ("switch7.png", "switch6.png"),
            model.Objects.SWORD: "rpg_sprite_gold9-5.png",
            model.Objects.TRAP_DOOR: "rpg_sprite_bw2-1.png",
            model.Objects.LIQUID1: "liquid3.png",
            model.Objects.LIQUID2: ("liquid_gold0.png", "liquid_gold1.png", "liquid_gold2.png", "liquid_gold3.png",
                                    "liquid_gold4.png", "liquid_gold5.png", "liquid_gold6.png", "liquid_gold7.png",
                                    "liquid_gold8.png", "liquid_gold9.png", "liquid_gold10.png", "liquid_gold11.png",
                                    "liquid_gold12.png", "liquid_gold13.png", "liquid_gold14.png", "liquid_gold15.png"
                                    ),
            model.Objects.LADDER_UP: "ladder2.png",
            model.Objects.LADDER_DOWN: "ladder1.png",
            model.Objects.WALL1: "winter_tiles0.png",
            model.Objects.WALL2: "winter_tiles2.png",
            model.Objects.WALL3: "winter_tiles3.png",

        })

        ImageManager.skins[new_skin_name] = new_skin

        new_skin_name = "World2"
        new_skin = (new_skin_name, {

            model.Objects.WALL1: "brick2.png",
            model.Objects.ENEMY1: "rpg_sprite_bw5-15.png",
            model.Objects.ENEMY2: "rpg_sprite_bw6-15.png",
            model.Objects.FAKE_WALL: "brick2.png",
            model.Objects.TILE1: "tile3.png",
            model.Objects.TILE2: "tile3.png",
            model.Objects.TILE3: "tile3.png",
            model.Objects.TILE4: "tile3.png",
            model.Objects.MONSTER1: "tile3.png",
            model.Objects.MONSTER2: "winter_tiles0.png",
            model.Objects.SWITCH_1: ("switch9.png", "switch8.png"),
            model.Objects.SWITCH_2: ("switch7.png", "switch6.png"),
            model.Objects.SWITCH_3: ("switch9.png", "switch8.png"),
            model.Objects.SWITCH_4: ("switch7.png", "switch6.png"),
        })

        ImageManager.skins[new_skin_name] = new_skin

        new_skin_name = "New Tiles"
        new_skin = (new_skin_name, {

            model.Objects.WALL1: "tiles64:5.png",
            model.Objects.FAKE_WALL: "tiles64:5.png",
            model.Objects.TILE1: "tiles64:2.png",
            model.Objects.TILE2: "tiles64:1.png",
            model.Objects.TILE3: "tiles64:2.png",
            model.Objects.TILE4: "tiles64:3.png",
        })

        ImageManager.skins[new_skin_name] = new_skin

        new_skin_name = "tutorial"
        new_skin = (new_skin_name, {

            model.Objects.WALL1: "rpg_sprite_bw8-1.png",
            model.Objects.BLOCK1: "rpg_sprite_bw9-0.png",
            model.Objects.BLOCK2: "rpg_sprite_bw6-1.png",
            model.Objects.ENEMY1: "rpg_sprite_gold5-15.png",
            model.Objects.ENEMY2: "rpg_sprite_gold8-17.png",
            model.Objects.FAKE_WALL: "rpg_sprite_bw8-1.png",
            model.Objects.TILE1: "tile20.png",
            model.Objects.MONSTER1: "tile20.png",
            model.Objects.MONSTER2: "tile20.png",
            model.Objects.PLAYER: ("knight_light0.png", "knight_light1.png", "knight_light2.png", "knight_light3.png"),
            model.Objects.PLAYER2: ("knight_light4.png", "knight_light5.png", "knight_light6.png", "knight_light7.png"),
            model.Objects.NPC1: "rpg_sprite_gold0-15.png",
            model.Objects.NPC2: "rpg_sprite_gold1-15.png",
            model.Objects.SWITCH_1: ("switch9.png", "switch8.png"),
            model.Objects.SWITCH_2: ("switch7.png", "switch6.png"),
            model.Objects.SWITCH_3: ("switch9.png", "switch8.png"),
            model.Objects.SWITCH_4: ("switch7.png", "switch6.png"),
            model.Objects.TREASURE: "rpg_sprite_gold7-12.png",
            model.Objects.DOOR1: "door0.png",
            model.Objects.DOOR1_OPEN: "door1.png",
        })

        ImageManager.skins[new_skin_name] = new_skin

        new_skin_name = "tutorial2"
        new_skin = (new_skin_name, {
            model.Objects.DECOR1: "rpg_sprite_gold3-17.png",
            model.Objects.DECOR2: "rpg_sprite_gold4-2.png",
            model.Objects.ENEMY1: "rpg_sprite_bw5-15.png",
            model.Objects.ENEMY2: "rpg_sprite_bw0-17.png",
            model.Objects.WALL1: "rpg_sprite_gold8-1.png",
            model.Objects.WALL2: "hieroglyph_light4.png",
            model.Objects.WALL3: "hieroglyph_light3.png",
            model.Objects.FAKE_WALL: "hieroglyph_light6.png",
            model.Objects.BLOCK1: "rpg_sprite_gold7-1.png",
            model.Objects.BLOCK2: "rpg_sprite_gold6-1.png",
            model.Objects.TILE1: "hieroglyph_dark2.png",
            model.Objects.TILE2: "hieroglyph_dark0.png",
            model.Objects.TILE3: "hieroglyph_dark4.png",
            model.Objects.TILE4: "hieroglyph_light6.png",
            model.Objects.TREASURE: "rpg_sprite_bw7-12.png",
            model.Objects.TREASURE_CHEST: "rpg_sprite_bw2-3.png",
            model.Objects.MONSTER1: "hieroglyph_dark1.png",
            model.Objects.MONSTER2: "hieroglyph_dark1.png",
            model.Objects.NPC1: "rpg_sprite_bw0-15.png",
            model.Objects.NPC2: "rpg_sprite_bw8-14.png",
            model.Objects.SWITCH_1: ("switch9.png", "switch8.png"),
            model.Objects.SWITCH_2: ("switch7.png", "switch6.png"),
            model.Objects.SWITCH_3: ("switch9.png", "switch8.png"),
            model.Objects.SWITCH_4: ("switch7.png", "switch6.png"),
            model.Objects.DOOR1: "rpg_sprite_gold2-2.png",
            model.Objects.DOOR1_OPEN: None,
            model.Objects.DOOR2: "rpg_sprite_gold1-2.png",
            model.Objects.DOOR2_OPEN: None,
            model.Objects.LADDER_UP: "ladder3.png",
            model.Objects.LADDER_DOWN: "ladder4.png",
            model.Objects.KEY: "rpg_sprite_bw7-3.png",
            model.Objects.BOSS_KEY: "rpg_sprite_bw9-3.png",

        })

        ImageManager.skins[new_skin_name] = new_skin

        new_skin_name = "world10"
        new_skin = (new_skin_name, {

            model.Objects.WALL1: "winter_tiles0.png",
            model.Objects.FAKE_WALL: "winter_tiles0.png",
            model.Objects.TREASURE: "rpg_sprite_gold7-12.png",
            model.Objects.TREASURE_CHEST: "rpg_sprite_gold2-3.png",
            model.Objects.DECOR1: "rpg_sprite_bw1-1.png",
            model.Objects.DECOR2: "rpg_sprite_bw6-2.png",
            model.Objects.DOOR1: "rpg_sprite_bw2-2.png",
            model.Objects.DOOR1_OPEN: None,
            model.Objects.DOOR2: "rpg_sprite_bw1-2.png",
            model.Objects.DOOR2_OPEN: None,
            model.Objects.ENEMY1: "rpg_sprite_gold4-17.png",
            model.Objects.ENEMY2: "rpg_sprite_gold5-17.png",
            model.Objects.LADDER_UP: "ladder3.png",
            model.Objects.LADDER_DOWN: "ladder4.png",
            model.Objects.LIQUID1: "rpg_sprite_bw0-3.png",
            model.Objects.LIQUID2: ("liquid_gold0.png", "liquid_gold1.png", "liquid_gold2.png", "liquid_gold3.png",
                                    "liquid_gold4.png", "liquid_gold5.png", "liquid_gold6.png", "liquid_gold7.png"),
            model.Objects.MONSTER1: "tile3.png",
            model.Objects.MONSTER2: "tile3.png",
            model.Objects.PLAYER: ("knight_light0.png", "knight_light1.png", "knight_light2.png", "knight_light3.png"),
            model.Objects.PLAYER2: ("knight_light4.png", "knight_light5.png", "knight_light6.png", "knight_light7.png"),
            model.Objects.TILE1: "tile3.png",
            model.Objects.TILE2: "tile3.png",
            model.Objects.TILE4: "tile2.png",

        })

        ImageManager.skins[new_skin_name] = new_skin

        new_skin_name = "dungeon"
        new_skin = (new_skin_name, {
            model.Objects.BLOCK1: "rpg_sprite_bw9-0.png",
            model.Objects.BLOCK2: "rpg_sprite_bw6-1.png",
            model.Objects.DECOR1: "rpg_sprite_gold0-13.png",
            model.Objects.DECOR2: "rpg_sprite_gold8-12.png",
            model.Objects.DOOR1: "rpg_sprite_bw2-2.png",
            model.Objects.DOOR1_OPEN: None,
            model.Objects.DOOR2: "rpg_sprite_bw1-2.png",
            model.Objects.DOOR2_OPEN: None,
            model.Objects.LADDER_DOWN: "ladder4.png",
            model.Objects.LADDER_UP: "ladder3.png",
            model.Objects.KEY: "key3.png",
            model.Objects.PLAYER: ("knight_light0.png", "knight_light1.png", "knight_light2.png", "knight_light3.png"),
            model.Objects.PLAYER2: ("knight_light4.png", "knight_light5.png", "knight_light6.png", "knight_light7.png"),
            model.Objects.ENEMY1: "rpg_sprite_gold5-15.png",
            model.Objects.ENEMY2: "rpg_sprite_gold3-18.png",
            model.Objects.NPC1: "rpg_sprite_gold5-14.png",
            model.Objects.TILE1: "basic_brick:2.png",
            model.Objects.TILE2: "wall2-64.png",
            model.Objects.TILE3: "tile4.png",
            model.Objects.TILE4: "rpg_sprite_bw8-2.png",
            model.Objects.TREASURE: "rpg_sprite_gold4-13.png",
            model.Objects.WALL1: "winter_tiles0.png",
            model.Objects.WALL2: "winter_tiles3.png",
            model.Objects.WALL3: "winter_tiles2.png",
            model.Objects.FAKE_WALL: "winter_tiles3.png",
        })

        ImageManager.skins[new_skin_name] = new_skin

        new_skin_name = "hub"
        new_skin = (new_skin_name, {
            model.Objects.DECOR1: "rpg_sprite_gold3-17.png",
            model.Objects.DECOR2: "rpg_sprite_gold4-2.png",
            model.Objects.ENEMY1: "rpg_sprite_bw5-15.png",
            model.Objects.ENEMY2: "rpg_sprite_bw0-17.png",
            model.Objects.WALL1: "winter_tiles0.png",
            model.Objects.WALL2: "winter_tiles2.png",
            model.Objects.WALL3: "winter_tiles3.png",
            model.Objects.FAKE_WALL: "hieroglyph_light6.png",
            model.Objects.BLOCK1: "rpg_sprite_gold7-1.png",
            model.Objects.BLOCK2: "rpg_sprite_gold6-1.png",
            model.Objects.TILE1: "rpg_sprite_green0-1.png",
            model.Objects.TILE2: "rpg_sprite_green1-1.png",
            model.Objects.TILE3: "tile3.png",
            model.Objects.TILE4: "rpg_sprite_green1-1.png",
            model.Objects.TRAP: "trap1.png",
            model.Objects.TREASURE: "rpg_sprite_bw7-12.png",
            model.Objects.TREASURE_CHEST: "rpg_sprite_bw2-3.png",
            model.Objects.MONSTER1: "hieroglyph_dark1.png",
            model.Objects.MONSTER2: "hieroglyph_dark1.png",
            model.Objects.NPC1: "rpg_sprite_bw0-15.png",
            model.Objects.NPC2: "rpg_sprite_bw8-14.png",
            model.Objects.SWITCH_1: ("switch9.png", "switch8.png"),
            model.Objects.SWITCH_2: ("switch7.png", "switch6.png"),
            model.Objects.SWITCH_3: ("switch9.png", "switch8.png"),
            model.Objects.SWITCH_4: ("switch7.png", "switch6.png"),
            model.Objects.DOOR1: "rpg_sprite_green1-2.png",
            model.Objects.DOOR1_OPEN: None,
            model.Objects.DOOR2: "rpg_sprite_green5-2.png",
            model.Objects.DOOR2_OPEN: None,
            model.Objects.LADDER_UP: "ladder3.png",
            model.Objects.LADDER_DOWN: "ladder4.png",
            model.Objects.KEY: "rpg_sprite_bw7-3.png",
            model.Objects.BOSS_KEY: "rpg_sprite_bw9-3.png",
        })

        ImageManager.skins[new_skin_name] = new_skin

    def get_skin_image(self, tile_name: str, skin_name: str = DEFAULT_SKIN, tick=0, width: int = 32, height: int = 32):

        if skin_name not in ImageManager.skins.keys():
            raise Exception("Can't find specified skin {0}".format(skin_name))

        name, tile_map = ImageManager.skins[skin_name]

        if tile_name not in tile_map.keys():
            name, tile_map = ImageManager.skins[ImageManager.DEFAULT_SKIN]
            if tile_name not in tile_map.keys():
                raise Exception("Can't find tile name '{0}' in skin '{1}'!".format(tile_name, skin_name))

        tile_file_names = tile_map[tile_name]

        image = None

        if tile_file_names is None:
            image = None
        elif isinstance(tile_file_names, tuple):
            if tick == 0:
                tile_file_name = tile_file_names[0]
            else:
                tile_file_name = tile_file_names[tick % len(tile_file_names)]

            image = self.get_image(image_file_name=tile_file_name, width=width, height=height)

        else:
            image = self.get_image(tile_file_names, width=width, height=height)

        return image

    def load_sprite_sheets(self):

        sheet_file_name = "tiles64x64.png"
        for i in range(0, 7):
            self.sprite_sheets["tiles64:{0}.png".format(i)] = (sheet_file_name, (i * 64, 0, 64, 64))

        sheet_file_name = "basic_brick2.png"
        for i in range(0, 4):
            self.sprite_sheets["basic_brick:{0}.png".format(i)] = (sheet_file_name, (i * 64, 0, 64, 64))

        sheet_file_name = "brick_tiles_1.png"
        for i in range(0, 5):
            self.sprite_sheets["brick{0}.png".format(i)] = (sheet_file_name, (i * 33 + 1, 1, 32, 32))

        sheet_file_name = "token.png"
        for i in range(0, 5):
            self.sprite_sheets["token{0}.png".format(i)] = (sheet_file_name, (i * 8, 0, 8, 8))

        sheet_file_name = "ladders_sheet2.png"
        for i in range(0, 5):
            self.sprite_sheets["ladder{0}.png".format(i)] = (sheet_file_name, (0, i * 32, 32, 32))

        sheet_file_name = "liquid_gold_sheet.png"
        for i in range(0, 16):
            self.sprite_sheets["liquid_gold{0}.png".format(i)] = (sheet_file_name, (i * 32, 0, 32, 32))

        sheet_file_name = "switches_sheet.png"
        for i in range(0, 10):
            self.sprite_sheets["switch{0}.png".format(i)] = (sheet_file_name, (i * 32, 0, 32, 32))

        sheet_file_name = "doors_sheet.png"
        for i in range(0, 4):
            self.sprite_sheets["door{0}.png".format(i)] = (sheet_file_name, (i * 32, 0, 32, 32))

        sheet_file_name = "trap_sheet.png"
        for i in range(0, 8):
            self.sprite_sheets["trap{0}.png".format(i)] = (sheet_file_name, (i * 32, 0, 32, 32))

        sheet_file_name = "hieroglyph_sheet2.png"
        i = 0
        for y in range(0, 4):
            for x in range(0, 4):
                self.sprite_sheets["hieroglyph_dark{0}.png".format(i)] = (sheet_file_name, (x * 33, y * 33, 32, 32))
                i += 1

        sheet_file_name = "hieroglyph_sheet3.png"
        i = 0
        for y in range(0, 4):
            for x in range(0, 4):
                self.sprite_sheets["hieroglyph_light{0}.png".format(i)] = (sheet_file_name, (x * 33, y * 33, 32, 32))
                i += 1

        sheet_file_name = "rpg_sheet_gold.png"
        for y in range(0, 21):
            for x in range(0, 10):
                self.sprite_sheets["rpg_sprite_gold{0}-{1}.png".format(x, y)] = (
                    sheet_file_name, (x * 32, y * 32, 32, 32))

        sheet_file_name = "rpg_sheet_bw.png"
        for y in range(0, 21):
            for x in range(0, 10):
                self.sprite_sheets["rpg_sprite_bw{0}-{1}.png".format(x, y)] = (
                    sheet_file_name, (x * 32, y * 32, 32, 32))

        sheet_file_name = "rpg_sheet_bw.png"
        for y in range(0, 21):
            for x in range(0, 10):
                self.sprite_sheets["rpg_sprite_green{0}-{1}.png".format(x, y)] = (
                    sheet_file_name, (x * 32, y * 32, 32, 32))

        sheet_file_name = "winter_sheet2.png"
        for i in range(0, 5):
            self.sprite_sheets["winter_tiles{0}.png".format(i)] = (sheet_file_name, (i * 119, 1, 96, 96))

        sheet_file_name = "knights64.png"
        for i in range(0, 8):
            self.sprite_sheets["knight_bw{0}.png".format(i)] = (sheet_file_name, (i * 64 + 8, 0, 48, 64))

        sheet_file_name = "knights64-2.png"
        for i in range(0, 8):
            self.sprite_sheets["knight_light{0}.png".format(i)] = (sheet_file_name, (i * 64 + 8, 0, 48, 64))

        # sheet_file_name = "knights2.png"
        # for i in range(0, 8):
        #     self.sprite_sheets["knight_light{0}.png".format(i)] = (sheet_file_name, (i * 32 + 4,0,24,32))


class View():
    image_manager = ImageManager()

    def __init__(self, width: int = 0, height: int = 0):
        self._debug = False
        self.tick_count = 0
        self.height = height
        self.width = width
        self.surface = None

        View.image_manager.initialise()

    def initialise(self):
        pass

    def tick(self):
        self.tick_count += 1

    def debug(self, debug_on: bool = None):

        if debug_on is None:
            self._debug = not self._debug
        else:
            self._debug = debug_on

    def process_event(self, new_event: model.Event):
        print("Default View Class event process:{0}".format(new_event))

        if new_event.type == Event.DEBUG:
            self.debug()

    def draw(self):
        pass


class DWMainFrame(View):
    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    TRANSPARENT = (0, 255, 0)

    def __init__(self, model: model.DWModel):

        super().__init__()

        self._debug = False

        self.model = model
        self.surface = None
        self.width = 600
        self.height = 600
        self._debug = False

        # Create a view for rendering the model of the current world
        # Define how far away the camera is allowed to follow the player by setting min and max positions
        # self.world_view = DWWorldView(self.model, min_view_pos=(200, -200, -350), max_view_pos=(800, 800, 400))
        self.world_view = DWWorldView(self.model, min_view_pos=(200, 200, -350), max_view_pos=(500, 500, 400))
        self.inventory_view = DWInventoryView(self.model)
        self.text_box = DWTextBox("")
        self.world_complete_view = DWWorldCompleteView(self.model)
        self.game_loaded_view = DWWorldGameLoaded(self.model)

    def initialise(self):

        super().initialise()

        print("Initialising {0}".format(__class__))

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption(self.model.name)

        self.surface = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWACCEL)

        filename = DWMainFrame.RESOURCES_DIR + "icon.png"

        try:
            image = pygame.image.load(filename)
            image = pygame.transform.scale(image, (32, 32))
            pygame.display.set_icon(image)
        except Exception as err:
            print(str(err))

        self.world_view.initialise()
        self.inventory_view.initialise()
        self.text_box.initialise()
        self.world_complete_view.initialise()
        self.game_loaded_view.initialise()

    def print(self):

        print("Printing Dark Work view...")
        self.world_view.print()
        self.inventory_view.print()
        self.text_box.print()
        self.world_complete_view.print()
        self.game_loaded_view.print()

    def inventory_show(self, view_on=None):
        if view_on is None:
            self.inventory_view.is_visible = not self.inventory_view.is_visible
        else:
            self.inventory_view.is_visible = view_on

    def draw(self):

        pane_rect = self.surface.get_rect()

        x = 0
        y = 0

        # Draw the main view of the world
        self.world_view.draw()
        self.surface.blit(self.world_view.surface, (x, y))

        x = self.world_view.width - self.inventory_view.width - 4
        y = 4

        # If the Inventory view is active then draw it
        if self.model.state == model.DWModel.STATE_PLAYING and self.inventory_view.is_visible is True:
            self.inventory_view.draw()
            self.surface.blit(self.inventory_view.surface, (x, y))

        # Draw the number of remaining lives
        img = View.image_manager.get_skin_image(tile_name=model.Objects.PLAYER, width=32, height=32)
        img = pygame.transform.scale(img, (int(img.get_rect().width / 2), int(img.get_rect().height / 2)))
        for i in range(0, self.model.player_lives):
            self.surface.blit(img, (i * 32 + 8, self.world_view.surface.get_rect().height - 32))

        # Draw the game state if we are not playing
        if self.model.state != model.DWModel.STATE_PLAYING:
            msg_box_width = 200
            msg_box_height = 64
            msg_rect = pygame.Rect((self.world_view.width - msg_box_width) / 2,
                                   (self.world_view.height - msg_box_height) / 2, msg_box_width, msg_box_height)

            pygame.draw.rect(self.surface,
                             Colours.DARK_GREY,
                             msg_rect,
                             0)

            pygame.draw.rect(self.surface,
                             Colours.LIGHT_GREY,
                             msg_rect,
                             2)

            draw_text(surface=self.surface,
                      msg="{0}".format(self.model.state),
                      x=self.world_view.width / 2,
                      y=self.world_view.height / 2,
                      size=32,
                      centre=True,
                      fg_colour=Colours.LIGHT_GREY,
                      bg_colour=Colours.DARK_GREY)

            # Draw the name of the current world
            if self.model.world is not None:
                msg_box_width = 260
                msg_box_height = 34
                y = 20

                msg_rect = pygame.Rect((self.world_view.width - msg_box_width) / 2,
                                       y, msg_box_width, msg_box_height)

                pygame.draw.rect(self.surface,
                                 Colours.DARK_GREY,
                                 msg_rect,
                                 0)

                pygame.draw.rect(self.surface,
                                 Colours.LIGHT_GREY,
                                 msg_rect,
                                 2)

                msg = "  {0}  ".format(self.model.world.name)
                draw_text(surface=self.surface, msg=msg,
                          x=self.width / 2,
                          y=y + msg_box_height / 2,
                          size=32,
                          fg_colour=Colours.LIGHT_GREY,
                          bg_colour=Colours.DARK_GREY)

            if self.model.state == model.DWModel.STATE_WORLD_COMPLETE:
                self.world_complete_view.draw()
                view_rect = self.world_complete_view.surface.get_rect()
                view_rect.center = pane_rect.center
                self.surface.blit(self.world_complete_view.surface, view_rect)

            elif self.model.state == model.DWModel.STATE_LOADED:
                self.game_loaded_view.draw()
                view_rect = self.game_loaded_view.surface.get_rect()
                view_rect.center = pane_rect.center
                self.surface.blit(self.game_loaded_view.surface, view_rect)

        # If the text box is active then draw it
        if self.text_box.is_visible is True:
            if self.model.state == model.DWModel.STATE_LOADED:
                self.text_box.width = 200
            else:
                self.text_box.width = 130
            self.text_box.draw()
            text_rect = self.text_box.surface.get_rect()
            if self.model.state == model.DWModel.STATE_LOADED:
                text_rect.centerx = pane_rect.centerx
                text_rect.bottom = view_rect.bottom - 10
            else:
                text_rect.topleft = pane_rect.topleft

            self.surface.blit(self.text_box.surface, text_rect)

    def update(self):
        pygame.display.update()

    def end(self):
        pygame.quit()
        print("Ending {0}".format(__class__))

    def tick(self):

        super().tick()

        self.world_view.tick()
        self.text_box.tick()
        self.world_complete_view.tick()
        self.game_loaded_view.tick()

    def process_event(self, new_event: model.Event):

        super().process_event(new_event)

        self.world_view.process_event(new_event)
        self.text_box.process_event(new_event)

        if self.model.state == model.DWModel.STATE_LOADED:
            self.text_box.fade_out = DWTextBox.FADE_IN_OUT
        elif self.model.state == model.DWModel.STATE_PLAYING:
            self.text_box.fade_out = DWTextBox.FADE_OUT
        elif self.model.state == model.DWModel.STATE_READY:
            self.text_box.fade_out = DWTextBox.FADE_IN_OUT
        elif self.model.state == model.DWModel.STATE_PAUSED:
            self.text_box.fade_out = DWTextBox.FADE_OUT
        elif self.model.state == model.DWModel.STATE_GAME_OVER:
            self.text_box.fade_out = DWTextBox.FADE_OUT
        else:
            self.text_box.fade_out = DWTextBox.FADE_OFF

    def move_view(self, direction):
        self.world_view.move_view(direction)


class DWWorldView(View):
    MAX_ZOOM = 2.0
    MIN_ZOOM = 0.8

    def __init__(self, model: model.DWModel, min_view_pos, max_view_pos, view_pos=None):

        super(DWWorldView, self).__init__()

        # Connect to the model
        self.model = model

        self.surface = None

        # Multiplication factor for size of images
        self.object_zoom_ratio = 1.0

        #  How big a view are we going to render?
        # self.width = 600 * self.object_size_scale
        # self.height = 600 * self.object_size_scale
        self.width = 600
        self.height = 600

        # How far away from the camera are we rendering objects before they disappear?
        self.depth = 65

        # How far above the player is the camera?
        self.camera_distance = -20

        # What are the constraints to the view position
        self.max_view_pos = np.array(max_view_pos)
        # self.max_view_pos = np.maximum(np.array(max_view_pos), np.array(([0,0,self.model.world.depth + self.camera_distance])))
        self.min_view_pos = np.array(min_view_pos)
        if view_pos is None:
            view_pos = np.add(self.min_view_pos, self.max_view_pos)
            view_pos = np.divide(view_pos, 2).astype(int)

        # Move the camera to the initial view point
        self.set_view(view_pos)

        # Set up helper class to translate model coordinates to view coordinates
        self.m2v = ModelToView3D(self.model)
        self.infinity = self.m2v.infinity

    def initialise(self):

        super(DWWorldView, self).initialise()

        print("Initialising {0}".format(__class__))
        self.surface = pygame.Surface((self.width, self.height))

    def print(self):

        print("Printing Dark Work Floor view...")
        print("View Pos = {0}\nPlayer pos = {1}".format(self.view_pos, self.model.world.player.xyz))

    def draw(self):

        self.surface.fill(Colours.BLACK)
        #self.surface.fill((200,200,200))

        if self.model.world is None:
            return

        # Get what skin we are using for the world that we are drawing
        self.skin = self.model.get_skin_name()

        # Find out where the player currently is
        vx, vy, vz = self.model.world.get_player_xyz()
        pz = vz

        # Move the camera relative to the players position
        vz += self.camera_distance

        # Set the view at the position and adjust vx,vy,vz accordingly
        vx,vy,vz = self.set_view((vx, vy, vz))

        # Get the visible objects at this view point from the model
        objs = self.m2v.get_object_list((vx, vy, vz),
                                        self.width / self.object_zoom_ratio,
                                        self.height / self.object_zoom_ratio,
                                        self.depth)

        # Draw visible objects in reverse order by distance from the camera
        distance = sorted(list(objs.keys()), reverse=True)

        # For each plane away from the camera...
        for d in distance:

            objs_at_d = objs[d]

            # For each object found in that plane...
            for pos, obj in objs_at_d:

                object_name = obj.name

                if obj.is_switch is True:
                    tick_count = obj.state
                elif obj.name == model.Objects.PLAYER:
                    dx, dy, dz = obj.dxyz
                    tick_count = obj.tick_count // 6
                    # If player is moving up the screen then swap to different set of images
                    if dy < 0:
                        object_name = model.Objects.PLAYER2
                else:
                    tick_count = self.tick_count

                # Get the image for the object based on the object's name
                image = View.image_manager.get_skin_image(object_name,
                                                          skin_name=self.skin,
                                                          tick=tick_count)

                # If we got an image...
                if image is not None:
                    # Get the object's position in the view
                    x, y, z = pos

                    # Scale the object based on the size of the object and how far away from the camera it is
                    # Size adjust = 1 on the plane that the player is currently on
                    size_adj = (1 - (d + self.camera_distance) / self.infinity) * self.object_zoom_ratio
                    size_w = int(obj.rect.width * size_adj)
                    size_h = int(obj.rect.height * size_adj)
                    image = pygame.transform.scale(image, (size_w, size_h))

                    # Change the image's transparency based on how far away from the player's plane it is
                    # Player's plane = opaque (alpha = 255)
                    # Between player and camera - increasing transparency the closer to the camera you get
                    # Beyond the player's plane - increasing levels of transparency until you reach the max depth of the view
                    # alpha = 255 * (1 - min((abs(pz-d-vz)*20/self.m2v.infinity, 1)))
                    alpha = 255 * (1 - min((abs(pz - d - vz) / self.depth, 1)))

                    # If we are drawing the player then check for special effects to change alpha
                    if obj.name == model.Objects.PLAYER:
                        if Event.EFFECT_INVISIBLE in self.model.world.effects:
                            alpha = 90
                        elif Event.EFFECT_PROTECTION in self.model.world.effects:
                            alpha = 255 - (self.tick_count % 6) * 40
                            # alpha = 255
                        elif Event.EFFECT_KILL_ENEMIES in self.model.world.effects:
                            pass

                    # If we are drawing an enemy then check for special effects
                    elif obj.name in model.World3D.ENEMIES:
                        if Event.EFFECT_FREEZE_ENEMIES in self.model.world.effects:
                            alpha = 255 - (self.tick_count % 6) * 40

                    image.set_alpha(alpha)

                    # Blit the object image at the appropriate place and size
                    image_rect = pygame.Rect(int(x * self.object_zoom_ratio), int(y * self.object_zoom_ratio), size_w,
                                             size_h)
                    self.surface.blit(image, image_rect)

                    # If we have drawn the player then check for special effects to draw these as well
                    if obj.name == model.Objects.PLAYER:
                        effect_image_name = None
                        if Event.EFFECT_INVISIBLE in self.model.world.effects:
                            effect_image_name = None
                        elif Event.EFFECT_PROTECTION in self.model.world.effects:
                            effect_image_name = model.Objects.HELMET1
                        elif Event.EFFECT_MELEE_ATTACK in self.model.world.effects:
                            effect_image_name = model.Objects.SWORD
                        elif Event.EFFECT_KILL_ENEMIES in self.model.world.effects:
                            effect_image_name = model.Objects.SWORD

                        if effect_image_name is not None:
                            # Get the image for the object based on the object's name
                            effect_image = View.image_manager.get_skin_image(effect_image_name,
                                                                             skin_name=self.skin,
                                                                             tick=tick_count)

                            effect_image = pygame.transform.scale(effect_image, (size_w, size_h))

                            # Centre effect image vs. player image
                            effect_rect = effect_image.get_rect()
                            effect_rect.center = image_rect.center

                            # alpha = 220 - (self.tick_count % 6) * 40
                            alpha = 220 - (tick_count % 6) * 40
                            effect_image.set_alpha(alpha)

                            if effect_image_name == model.Objects.SWORD:
                                effect = self.model.get_effect(Event.EFFECT_MELEE_ATTACK)
                                if effect is not None:
                                    type, count, duration = effect
                                    # effect_image = pygame.transform.rotate(effect_image, 45 + 180 * count / duration)
                                    effect_image.set_alpha(255)

                                    odx, ody, odz = obj.dxyz

                                    effect_rect.centerx += (odx * 8 * (1 - count / duration))
                                    effect_rect.centery += (ody * 8 * (1 - count / duration))
                                    # print("{0}: xyz={1}, oxyz={2}, dxyz={3}".format(obj.name, obj.xyz, obj.old_xyz, obj.dxyz))
                                    # pygame.draw.line(self.surface,
                                    #                  Colours.YELLOW,
                                    #                  image_rect.center,
                                    #                  (image_rect.centerx + odx * 16, image_rect.centery + ody * 16),
                                    #                  4)
                                    if self._debug is True:
                                        hit_box = self.model.get_melee_hit_box().rect
                                        vx, vy, vz = self.m2v.model_to_view_xyz(view_pos=self.view_pos, \
                                                                                view_width=self.width / self.object_zoom_ratio, \
                                                                                view_height=self.height / self.object_zoom_ratio, \
                                                                                model_xyz=(hit_box.x,hit_box.y,pz))

                                        pygame.draw.rect(self.surface,
                                                         Colours.WHITE,
                                                         (vx* self.object_zoom_ratio,vy* self.object_zoom_ratio,int(hit_box.width*size_adj),int(hit_box.height*size_adj)),
                                                         2)

                            # Centre effect image vs. player image
                            self.surface.blit(effect_image, effect_rect)

        if self._debug is True:

            # Draw current view position
            msg = "View Pos={0} : Distances={1} : Zoom {2:.2} : Tick={3}".format(self.view_pos,
                                                                                 str(distance),
                                                                                 self.object_zoom_ratio,
                                                                                 self.tick_count)
            text_rect = (0, 0, 300, 30)
            drawText(surface=self.surface,
                     text=msg,
                     color=Colours.GOLD,
                     rect=text_rect,
                     font=pygame.font.SysFont(pygame.font.get_default_font(), 12),
                     bkg=Colours.DARK_GREY)

            n = model.Navigator()
            to_obj = self.model.player
            for bot in self.model.world.bots:

                from_obj = bot.target_object

                r = n.navigate2(self.model.world, from_obj, to_obj)
                if r is True:
                    trace_colour = Colours.DARK_GREEN
                    point = to_obj.xyz
                    vx, vy, vz = self.m2v.model_to_view_xyz(view_pos=self.view_pos, \
                                                            view_width=self.width / self.object_zoom_ratio, \
                                                            view_height=self.height / self.object_zoom_ratio, \
                                                            model_xyz=point)

                    pygame.draw.rect(self.surface,
                                     trace_colour,
                                     (vx, vy, to_obj.rect.width, to_obj.rect.height),
                                     1)
                else:
                    trace_colour = pygame.Color(min(20 + len(n.hits) * 30, 255), 0, 0)
                    for blocker in n.blockers:
                        point = blocker.xyz
                        vx, vy, vz = self.m2v.model_to_view_xyz(view_pos=self.view_pos, \
                                                                view_width=self.width / self.object_zoom_ratio, \
                                                                view_height=self.height / self.object_zoom_ratio, \
                                                                model_xyz=point)

                        pygame.draw.rect(self.surface,
                                         trace_colour,
                                         (vx * self.object_zoom_ratio, vy * self.object_zoom_ratio, blocker.rect.width,
                                          blocker.rect.height),
                                         2)

                    # for point in n.route:
                    #     vx, vy, vz = self.m2v.model_to_view_xyz(view_pos=self.view_pos, \
                    #                                             view_width=self.width / self.object_zoom_ratio, \
                    #                                             view_height=self.height / self.object_zoom_ratio, \
                    #                                             model_xyz=point)
                    #     hit_box = pygame.Rect((0, 0), (model.Navigator.HIT_BOX_SIZE, model.Navigator.HIT_BOX_SIZE))
                    #     hit_box.centerx = vx
                    #     hit_box.centery = vy

                    # pygame.draw.rect(self.surface,
                    #                  trace_colour,
                    #                  (vx*self.object_zoom_ratio,vy*self.object_zoom_ratio,model.Navigator.HIT_BOX_SIZE,model.Navigator.HIT_BOX_SIZE),
                    #                  1)

                    # pygame.draw.rect(self.surface,
                    #                  trace_colour,
                    #                  hit_box,
                    #                  1)

        # msg = "  {0}  ".format(self.model.world.name)
        # draw_text(surface=self.surface, msg=msg, x=self.width / 2, y=20, size=32, fg_colour=Colours.WHITE,
        #           bg_colour=Colours.BLACK)

    def set_view(self, new_view_pos):

        # self.min_view_pos = np.divide(self.min_view_pos, self.object_zoom_ratio)
        # self.max_view_pos = np.divide(self.min_view_pos, self.object_zoom_ratio)
        # Set the position of the camera applying the minimum and maximum constraints of where is is allowed to go
        self.view_pos = np.clip(new_view_pos, self.min_view_pos, self.max_view_pos)

        return self.view_pos

    def move_view(self, direction):
        # Move the view camera in a specified direction but...
        # constrain where the camera can go using min and max positions
        new_view_pos = np.add(self.view_pos, direction)
        self.view_pos = np.clip(new_view_pos, self.min_view_pos, self.max_view_pos)

    def zoom_view(self, zoom_delta: float = None):
        # Change how much we zoom into the world view
        # object_zoom_ratio = 1.0 Normal View
        # Object_zoom_ratio > 1.0 Zoom in
        # Object_zoom_ratio < 1.0 zoom out
        if zoom_delta is None:
            self.object_zoom_ratio = 1.0
        else:
            self.object_zoom_ratio = max(min(self.object_zoom_ratio * (1 + zoom_delta), DWWorldView.MAX_ZOOM),
                                         DWWorldView.MIN_ZOOM)
            self.set_view(self.view_pos)


class ModelToView3D():
    """
    This class is a helper class that takes a 3D world and renders it onto a 2D plane
    """

    PERSPECTIVE = "perspective"
    PARALLEL = "parallel"

    def __init__(self, model):

        # Connect to the model
        self.model = model

        # How far away is infinity so we can calculate perspective?
        self.infinity = 500

        # How much space around the view do we want to add extra objects?
        self.view_padding = 128

        #  Add perspective to the position of objects in the view
        # self.projection = ModelToView3D.PARALLEL
        self.projection = ModelToView3D.PERSPECTIVE

    def get_object_list(self, view_pos, view_width, view_height, view_depth):

        # List for holding the objects that will be visible and where they are positioned relative to the camera
        objects = {}

        vx, vy, vz = view_pos

        # Calculate which planes in the world will be visible from the current camera position
        visible_planes = np.array(list(self.model.world.planes.keys()))
        visible_planes = visible_planes[visible_planes >= vz]
        visible_planes = visible_planes[visible_planes < (vz + view_depth)]

        # for each visible plane in the model world...
        for z in visible_planes:

            # Get the list of objects from the model that are at this plane...
            # objects_at_z = sorted(self.model.world.planes[z], key=lambda obj: obj.rect.y * 1000 + obj.rect.x)
            objects_at_z = self.model.world.planes[z]

            # For each object in the list...
            for obj in objects_at_z:

                if obj.is_visible is False:
                    continue

                # Calculate where the object's position is relative to the current camera view point
                ox, oy, oz = obj.xyz
                od = oz - vz
                ow = ox - vx
                oh = oy - vy

                # filter out objects that don't fit into the current camera view size (h, w, d)
                if abs(ow) > (view_width + self.view_padding) / 2 \
                        or abs(oh) > (view_height + self.view_padding) / 2:
                    pass
                # If the object fits into the current view...
                else:

                    # If we don't have a list of objects at this distance then create an empty one
                    if od not in objects.keys():
                        objects[od] = []

                    # Add the object's adjusted position and the object itself to our collection of objects in this plane
                    objects[od].append(((
                                            ow * (1 - od / self.infinity * (
                                                    self.projection == ModelToView3D.PERSPECTIVE)) + (
                                                    view_width / 2),
                                            oh * (1 - od / self.infinity * (
                                                    self.projection == ModelToView3D.PERSPECTIVE)) + (
                                                    view_height / 2),
                                            od),
                                        obj))

        return objects

    def model_to_view_xyz(self, view_pos, view_width, view_height, model_xyz):

        vx, vy, vz = view_pos
        mx, my, mz = model_xyz

        vz = (mz - vz)
        vx = (mx - vx) * (1 - vz / self.infinity * (self.projection == ModelToView3D.PERSPECTIVE)) + (view_width / 2)
        vy = (my - vy) * (1 - vz / self.infinity * (self.projection == ModelToView3D.PERSPECTIVE)) + (view_height / 2)

        return vx, vy, vz


class DWTextBox(View):
    FADE_OFF = "fade off"
    FADE_IN = "fade in"
    FADE_OUT = "fade out"
    FADE_IN_OUT = "fade in and out"

    def __init__(self, model: str):
        super().__init__()

        # Connect to the model
        self.model = model
        self.msg_queue = deque()
        self.surface = None

        # Properties of the text box
        self.width = 130
        self.height = 150
        self.margin = 4
        self.padding = 4
        self.skin = "default"
        self.text_size = 20
        self.fg = Colours.WHITE
        self.bg = Colours.BLACK
        self.timer = self.tick_count
        self.fade_out = DWTextBox.FADE_OFF
        self.life_time_ticks = 20

    @property
    def is_visible(self):
        return self.tick_count < (self.timer + self.life_time_ticks)

    def initialise(self, fade_out: str = FADE_OFF):
        super().initialise()

        print("Initialising {0}".format(__class__))
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_colorkey((0, 255, 0))
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), self.text_size)
        self.fade_out = fade_out
        self.set_size()

    def set_size(self):

        # Get the width of the text to be displayed
        fullWidth = self.font.size(self.model)[0]

        # get the maximum height of the font with some padding
        fontHeight = self.font.size("Tg")[1] + 2

        # How many line of text will we be displaying given the width of teh text box?
        lines = math.ceil(fullWidth / (self.width - (self.padding + self.margin)*2))

        # Calculate how high the text box needs to be
        self.height = lines * (fontHeight) + (self.margin + self.padding)*2

        #  Calculate rect for actual text
        self.text_rect = pygame.Rect(self.padding + self.margin,
                          self.padding + self.margin,
                          self.width - 2 * (self.padding + self.margin),
                          self.height - 2 * (self.padding + self.padding))

        # Calculate rect for border
        self.border_rect = pygame.Rect(self.padding,
                            self.padding,
                            self.width - 2 * self.padding,
                            self.height - 2 * self.padding)

        # Create a surface of the right size
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_colorkey((0, 255, 0))
        #print(f'text({self.model}), text w/h:{self.text_rect.width}/{self.text_rect.height}, full width = {fullWidth}, lines={lines}')


    def print(self):
        print("Printing Dark Work Text Box view: txt={0}, fade option = {1}".format(self.model, self.fade_out))
        print("Msg Q = {0}".format(str(self.msg_queue)))

    def tick(self):

        super().tick()

        if len(self.msg_queue) > 0:
            if self.tick_count > (self.timer + self.life_time_ticks):
                self.model = self.msg_queue.popleft()
                self.timer = self.tick_count

    def process_event(self, new_event: model.Event):

        super().process_event(new_event)

        if new_event.name in (Event.TALK, Event.READ):
            self.msg_queue.appendleft(new_event.description)
            self.model = self.msg_queue.popleft()
            self.timer = self.tick_count
        elif new_event.type == Event.STATE:
            self.msg_queue.appendleft(new_event.description)
            self.model = self.msg_queue.popleft()
            self.timer = self.tick_count
        else:
            self.msg_queue.append(new_event.description)

    def draw(self):
        self.set_size()

        if self.tick_count > (self.timer + self.life_time_ticks):
            return

        pygame.draw.rect(self.surface,
                         Colours.DARK_GREY,
                         self.border_rect,
                         0)

        pygame.draw.rect(self.surface,
                         Colours.WHITE,
                         self.border_rect,
                         2)

        drawText(surface=self.surface,
                 text=self.model,
                 rect=self.text_rect,
                 font=self.font,
                 color=self.fg,
                 bkg=self.bg)

        life_pct = (self.tick_count - self.timer) / self.life_time_ticks
        if self.fade_out == DWTextBox.FADE_OFF:
            alpha = 255
        elif self.fade_out == DWTextBox.FADE_IN:
            alpha = 255 * life_pct * 1.5
        elif self.fade_out == DWTextBox.FADE_OUT:
            alpha = 255 * (1 - life_pct) * 1.5
        elif self.fade_out == DWTextBox.FADE_IN_OUT:
            alpha = 255 * (1 - abs(1 - (life_pct * 2))) * 1.5

        self.surface.set_alpha(alpha)


class DWInventoryView(View):

    def __init__(self, model: model.DWModel):
        super().__init__()

        # Connect to the model
        self.model = model
        self.surface = None

        # Properties of the text box
        self.width = 100
        self.height = 300
        self.icon_size = 24
        self.text_size = 14
        self.margin = 4
        self.padding = 4
        self.skin = ImageManager.DEFAULT_SKIN
        self.fg = Colours.LIGHT_GREY
        self.bg = Colours.BLACK
        self.is_visible = True

    def initialise(self):
        super().initialise()

        print("Initialising {0}".format(__class__))
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_colorkey((0, 255, 0))
        self.set_size()

    def set_size(self):

        self.height = 32
        self.height += len(self.model.inventory.keys()) * self.icon_size

        self.border_rect = pygame.Rect(self.padding,
                                       self.padding,
                                       self.width - 2 * self.padding,
                                       self.height - 2 * self.padding)

        self.text_rect = pygame.Rect(self.padding + self.margin,
                                     self.padding + self.margin,
                                     self.width - 2 * (self.padding + self.margin),
                                     self.height - 2 * (self.padding + self.padding))

    def print(self):
        print("Printing Dark Work Inventory view...")

    def draw(self):

        self.surface.fill((0, 255, 0))

        self.set_size()

        if self.is_visible is False:
            return

        # Get what skin we are using for the world that we are drawing
        self.skin = self.model.get_skin_name()

        pygame.draw.rect(self.surface,
                         Colours.DARK_GREY,
                         self.border_rect,
                         0)

        pygame.draw.rect(self.surface,
                         Colours.WHITE,
                         self.border_rect,
                         2)

        x = self.text_rect.centerx
        y = self.text_rect.y + 8

        text = "Inventory:"
        draw_text(surface=self.surface, msg=text, x=x, y=y, size=18,
                  fg_colour=Colours.WHITE, bg_colour=Colours.DARK_GREY, centre=True)

        y -= 2
        x = self.text_rect.x + self.icon_size

        for item, count in self.model.inventory.items():

            if count > 0:
                y += self.icon_size

                img = View.image_manager.get_skin_image(tile_name=item, skin_name=self.skin)
                img = pygame.transform.scale(img, (self.icon_size, self.icon_size))
                self.surface.blit(img, (self.text_rect.x, y - int(self.icon_size / 2)))

                text = "{0} x {1}".format(item.title(), count)
                draw_text(surface=self.surface, msg=text, x=x, y=y + 6 - int(self.icon_size / 4), size=self.text_size,
                          fg_colour=Colours.WHITE, bg_colour=Colours.DARK_GREY, centre=False)


class DWWorldCompleteView(View):

    def __init__(self, model: model.DWModel):
        super().__init__()

        # Connect to the model
        self.model = model
        self.surface = None

        # Properties of the text box
        self.width = 400
        self.height = 300
        self.icon_size = 40
        self.text_size = 24
        self.margin = 6
        self.padding = 6
        self.skin = ImageManager.DEFAULT_SKIN
        self.fg = Colours.WHITE
        self.bg = Colours.DARK_GREY

    def initialise(self):
        super().initialise()

        print("Initialising {0}".format(__class__))
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_colorkey((0, 255, 0))
        self.set_size()

    def set_size(self):

        self.height += len(self.model.inventory.keys()) * self.icon_size

        self.border_rect = pygame.Rect(self.padding,
                                       self.padding,
                                       self.width - 2 * self.padding,
                                       self.height - 2 * self.padding)

        self.text_rect = pygame.Rect(self.padding + self.margin,
                                     self.padding + self.margin,
                                     self.width - 2 * (self.padding + self.margin),
                                     self.height - 2 * (self.padding + self.padding))

    def print(self):
        print("Printing {0} tick=({1})".format(__class__, self.tick_count))

    def draw(self):

        self.surface.fill(Colours.DARK_GREY)

        pane_rect = self.surface.get_rect()

        # Get what skin we are using for the world that we are drawing
        self.skin = self.model.get_skin_name()

        pygame.draw.rect(self.surface,
                         Colours.DARK_GREY,
                         self.border_rect,
                         0)

        pygame.draw.rect(self.surface,
                         Colours.LIGHT_GREY,
                         self.border_rect,
                         2)

        x = self.text_rect.centerx
        y = self.text_rect.y + 16

        text = "{0} Complete".format(self.model.world.name, self.tick_count)
        draw_text(surface=self.surface, msg=text, x=x, y=y, size=int(self.text_size * 1.5),
                  fg_colour=Colours.LIGHT_GREY, bg_colour=Colours.DARK_GREY, centre=True)

        img = View.image_manager.get_skin_image(tile_name=model.Objects.PLAYER, skin_name=self.skin,
                                                tick=self.tick_count)

        scale_factor = int((6 - 3* abs(1 - (self.tick_count % 50 / 25)))* self.icon_size)
        img = pygame.transform.scale(img, (scale_factor, scale_factor))

        alpha = int(255 * (1 - abs(1 - (self.tick_count % 50 / 25))))
        img.set_alpha(alpha)
        img_rect = img.get_rect()
        img_rect.centerx = pane_rect.centerx
        img_rect.bottom = pane_rect.bottom - 16
        self.surface.blit(img, img_rect)

        y = self.text_rect.y + self.text_size
        x = self.text_rect.x + self.icon_size

        # Display what you currently have in your inventory and the current value
        inventory_value = 0
        types_of_item = 0

        for item, count in self.model.inventory.items():

            if count > 0:
                types_of_item += 1

                item_object = model.WorldObjectLoader.get_object_copy_by_name(item)
                inventory_value += (item_object.value * count)

                y += (self.icon_size * (types_of_item % 2 == 1))

                img = View.image_manager.get_skin_image(tile_name=item, skin_name=self.skin)
                img = pygame.transform.scale(img, (self.icon_size, self.icon_size))
                self.surface.blit(img, (self.text_rect.x + (((types_of_item % 2) == 0) * self.text_rect.width / 2),
                                        y - int(self.icon_size / 2)))

                text = "{0} x {1}".format(item.title(), count)
                draw_text(surface=self.surface,
                          msg=text,
                          x=x + (((types_of_item % 2) == 0) * self.text_rect.width / 2),
                          y=y + 6 - int(self.icon_size / 4),
                          size=self.text_size,
                          fg_colour=Colours.LIGHT_GREY,
                          bg_colour=None,
                          centre=False)

        y = self.text_rect.bottom - (self.text_size * 1.0)
        text = "Inventory Value = {0}".format(inventory_value)
        draw_text(surface=self.surface, msg=text, x=self.text_rect.centerx, y=y, size=int(self.text_size * 1.5),
                  fg_colour=Colours.LIGHT_GREY, bg_colour=None, centre=True)

class DWWorldGameLoaded(View):

    def __init__(self, model: model.DWModel):
        super().__init__()

        # Connect to the model
        self.model = model
        self.surface = None

        # Properties of the text box
        self.width = 400
        self.height = 300
        self.icon_size = 40
        self.text_size = 24
        self.margin = 6
        self.padding = 6
        self.skin = ImageManager.DEFAULT_SKIN
        self.fg = Colours.WHITE
        self.bg = Colours.DARK_GREY

    def initialise(self):
        super().initialise()

        print("Initialising {0}".format(__class__))
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.set_colorkey((0, 255, 0))
        self.set_size()

    def set_size(self):

        self.height += len(self.model.inventory.keys()) * self.icon_size

        self.border_rect = pygame.Rect(self.padding,
                                       self.padding,
                                       self.width - 2 * self.padding,
                                       self.height - 2 * self.padding)

        self.text_rect = pygame.Rect(self.padding + self.margin,
                                     self.padding + self.margin,
                                     self.width - 2 * (self.padding + self.margin),
                                     self.height - 2 * (self.padding + self.padding))

    def print(self):
        print("Printing {0} tick=({1})".format(__class__, self.tick_count))

    def draw(self):

        self.surface.fill(Colours.DARK_GREY)

        pane_rect = self.surface.get_rect()

        # Get what skin we are using for the world that we are drawing
        self.skin = self.model.get_skin_name()

        pygame.draw.rect(self.surface,
                         Colours.DARK_GREY,
                         self.border_rect,
                         0)

        pygame.draw.rect(self.surface,
                         Colours.LIGHT_GREY,
                         self.border_rect,
                         2)

        x = self.text_rect.centerx
        y = self.text_rect.y + 32

        text = "Dark World"
        draw_text(surface=self.surface,
                  msg=text,
                  x=x,
                  y=y,
                  size=64,
                  fg_colour=Colours.LIGHT_GREY,
                  bg_colour=Colours.DARK_GREY,
                  centre=True)

        img = View.image_manager.get_skin_image(tile_name=model.Objects.NPC1, skin_name=self.skin,
                                                tick=self.tick_count)

        scale_factor = int((6 - 3* abs(1 - (self.tick_count % 100 / 50)))* self.icon_size)
        img = pygame.transform.scale(img, (scale_factor, scale_factor))

        img_alpha = int(255 * (1 - abs(1 - (self.tick_count % 100 / 50))))
        img.set_alpha(img_alpha)
        img_rect = img.get_rect()
        img_rect.centerx = pane_rect.centerx
        img_rect.centery =  pane_rect.centery - 10
        self.surface.blit(img, img_rect)




