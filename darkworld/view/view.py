import darkworld.model as model
from .graphics import *
import pygame
import os
import numpy as np
import logging
from operator import itemgetter
from darkworld.model.events import *


class Colours:
    # set up the colours
    BLACK = (0, 0, 0)
    BROWN = (128, 64, 0)
    WHITE = (255, 255, 255)
    RED = (237, 28, 36)
    GREEN = (34, 177, 76)
    BLUE = (63, 72, 204)
    DARK_GREY = (40, 40, 40)
    GREY = (128, 128, 128)
    GOLD = (255, 201, 14)
    YELLOW = (255, 255, 0)
    TRANSPARENT = (255, 1, 1)


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

                # image = pygame.transform.scale(original_image, (width, height))
                ImageManager.image_cache[image_file_name] = original_image
                logging.info("Image {0} loaded and scaled to {1}x{2} and cached.".format(filename, width, height))


            except Exception as err:
                print(str(err))

        return self.image_cache[image_file_name]

    def load_skins(self):

        new_skin_name = ImageManager.DEFAULT_SKIN
        new_skin = (new_skin_name, {

            model.Objects.EMPTY: None,
            model.Objects.WALL1: "winter_tiles0.png",
            model.Objects.WALL2: "winter_tiles2.png",
            model.Objects.WALL3: "winter_tiles3.png",
            model.Objects.FAKE_WALL: "wall.png",
            model.Objects.BOOK: "rpg_sprite2-5.png",
            model.Objects.COINS: "rpg_sprite_gold1-12.png",
            model.Objects.SCROLL: "rpg_sprite_gold0-5.png",
            model.Objects.ENEMY1: "rpg_sprite_bw5-15.png",
            model.Objects.ENEMY2: "rpg_sprite_bw6-15.png",
            model.Objects.EXTRA_LIFE: "rpg_sprite_gold1-14.png",
            model.Objects.BLOCK1: "block1.png",
            model.Objects.BLOCK2: "block2.png",
            model.Objects.PLAYER: ("robotA0000.png", "robotA0001.png", "robotA0002.png", "robotA0003.png"),
            model.Objects.HELMET1: "rpg_sprite_gold2-10.png",
            model.Objects.HELMET2: "rpg_sprite_gold3-10.png",
            model.Objects.MAP: "rpg_sprite1-5.png",
            model.Objects.MONSTER1: "bear.png",
            model.Objects.MONSTER2: "winter_tiles0.png",
            model.Objects.NPC1: "rpg_sprite_bw0-15.png",
            model.Objects.NPC2: "rpg_sprite_bw1-15.png",
            model.Objects.BIG_MONSTER1: "bear.png",
            model.Objects.BIG_MONSTER2: "winter_tiles0.png",
            model.Objects.BOMB: "rpg_sprite2-8.png",
            # model.Objects.PLAYER: ("man0.png", "man2.png", "man1.png", "man2.png"),
            # model.Objects.TREASURE: "treasure.png",
            model.Objects.TREASURE: ("token0.png", "token1.png", "token2.png", "token3.png"),
            model.Objects.TREASURE_CHEST: "treasure_chest.png",
            model.Objects.DECOR1: "rpg_sprite_gold0-13.png",
            model.Objects.DECOR2: "rpg_sprite_gold1-13.png",
            model.Objects.DOOR1: "door.png",
            model.Objects.DOOR1_OPEN: "door_open.png",
            model.Objects.TRAP: "trap.png",
            model.Objects.TRAP_DISABLE: "trap_disable.png",
            model.Objects.KEY: "key2.png",
            model.Objects.BOSS_KEY: "key4.png",
            model.Objects.TILE1: "tile1.png",
            model.Objects.TILE2: "tile2.png",
            model.Objects.TILE3: "tile3.png",
            model.Objects.TILE4: "tile4.png",
            model.Objects.TELEPORT: ("teleport_00.png", "teleport_01.png", "teleport_02.png"),
            model.Objects.HOLE: "down shoot.png",
            model.Objects.EXIT_NEXT: "exit_green.png",
            model.Objects.EXIT_PREVIOUS: "exit_red.png",
            model.Objects.POTION1: "rpg_sprite_gold5-4.png",
            model.Objects.POTION2: "rpg_sprite_gold4-4.png",
            model.Objects.SWITCH_TILE1: None,
            model.Objects.SWITCH_TILE2: None,
            model.Objects.SWITCH_TILE3: None,
            model.Objects.SWITCH_TILE4: None,
            model.Objects.SWITCH_1: ("switch0.png", "switch1.png"),
            model.Objects.SWITCH_2: ("switch1.png", "switch0.png"),
            model.Objects.SWITCH_3: ("switch0.png", "switch1.png"),
            model.Objects.SWITCH_4: ("switch1.png", "switch0.png"),
            model.Objects.SWORD: "rpg_sprite_gold9-5.png",
            model.Objects.LIQUID1: "liquid3.png",
            model.Objects.LIQUID2: "liquid2.png",
            model.Objects.LADDER_UP: "ladder2.png",
            model.Objects.LADDER_DOWN: "ladder1.png",

        })

        ImageManager.skins[new_skin_name] = new_skin

        new_skin_name = "World2"
        new_skin = (new_skin_name, {

            model.Objects.WALL1: "brick2.png",
            model.Objects.FAKE_WALL: "brick2.png",
            model.Objects.TILE1: "tile4.png",
            model.Objects.MONSTER1: "tile3.png",
            model.Objects.MONSTER2: "winter_tiles0.png",
            model.Objects.SWITCH_1: ("switch0.png", "switch3.png"),
            model.Objects.SWITCH_2: ("switch1.png", "switch2.png"),
            model.Objects.SWITCH_3: ("switch0.png", "switch3.png"),
            model.Objects.SWITCH_4: ("switch1.png", "switch2.png"),
        })

        ImageManager.skins[new_skin_name] = new_skin

        ImageManager.skins[new_skin_name] = new_skin

        new_skin_name = "tutorial"
        new_skin = (new_skin_name, {

            model.Objects.WALL1: "wall.png",
            model.Objects.FAKE_WALL: "wall.png",
            model.Objects.TILE1: "tile20.png",
            model.Objects.MONSTER1: "tile20.png",
            model.Objects.MONSTER2: "tile20.png",
            model.Objects.SWITCH_1: ("switch0.png", "switch5.png"),
            model.Objects.SWITCH_2: ("switch1.png", "switch4.png"),
            model.Objects.SWITCH_3: ("switch0.png", "switch5.png"),
            model.Objects.SWITCH_4: ("switch1.png", "switch4.png"),
            model.Objects.DOOR1: "door0.png",
            model.Objects.DOOR1_OPEN: "door1.png",
        })

        ImageManager.skins[new_skin_name] = new_skin

        new_skin_name = "tutorial2"
        new_skin = (new_skin_name, {

            model.Objects.WALL1: "hieroglyph_light5.png",
            model.Objects.WALL1: "rpg_sprite_gold8-1.png",
            model.Objects.WALL2: "hieroglyph_light4.png",
            model.Objects.WALL3: "hieroglyph_light3.png",
            model.Objects.FAKE_WALL: "hieroglyph_light6.png",
            model.Objects.BLOCK1: "rpg_sprite_gold7-1.png",
            model.Objects.BLOCK2: "rpg_sprite_gold6-1.png",
            model.Objects.TILE1: "hieroglyph_dark2.png",
            model.Objects.TILE2: "hieroglyph_dark0.png",
            model.Objects.TILE3: "hieroglyph_dark4.png",
            model.Objects.TILE4: "hieroglyph_dark6.png",
            model.Objects.TREASURE: "rpg_sprite7-12.png",
            model.Objects.TREASURE_CHEST: "rpg_sprite2-3.png",
            model.Objects.MONSTER1: "hieroglyph_dark1.png",
            model.Objects.MONSTER2: "hieroglyph_dark1.png",
            model.Objects.NPC2: "rpg_sprite_bw8-14.png",
            model.Objects.SWITCH_1: ("switch0.png", "switch5.png"),
            model.Objects.SWITCH_2: ("switch0.png", "switch5.png"),
            model.Objects.SWITCH_3: ("switch0.png", "switch5.png"),
            model.Objects.SWITCH_4: ("switch0.png", "switch5.png"),
            model.Objects.DOOR1: "rpg_sprite_gold2-2.png",
            model.Objects.DOOR1_OPEN: None,
            model.Objects.DOOR2: "rpg_sprite_gold1-2.png",
            model.Objects.DOOR2_OPEN: None,
            model.Objects.LADDER_UP: "ladder3.png",
            model.Objects.KEY: "rpg_sprite_gold7-3.png",
            model.Objects.BOSS_KEY: "rpg_sprite_gold9-3.png",

        })

        ImageManager.skins[new_skin_name] = new_skin

        new_skin_name = "dungeon"
        new_skin = (new_skin_name, {
            model.Objects.DECOR1: "rpg_sprite_gold0-13.png",
            model.Objects.DECOR2: "rpg_sprite_gold8-12.png",
            model.Objects.LADDER_DOWN: "ladder4.png",
            model.Objects.LADDER_UP: "ladder3.png",
            model.Objects.ENEMY1: "rpg_sprite_gold5-15.png",
            model.Objects.NPC1: "rpg_sprite_gold5-14.png",
            model.Objects.TILE1: "tile4.png",
            model.Objects.TILE2: "wall2.png",
            model.Objects.TREASURE:"rpg_sprite_gold1-12.png",
            model.Objects.WALL1: "winter_tiles0.png",
            model.Objects.WALL2: "winter_tiles3.png",
            model.Objects.WALL3: "winter_tiles2.png",
            model.Objects.FAKE_WALL: "winter_tiles0.png",
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

        sheet_file_name = "brick_tiles_1.png"
        for i in range(0, 5):
            self.sprite_sheets["brick{0}.png".format(i)] = (sheet_file_name, (i * 33 + 1, 1, 32, 32))

        sheet_file_name = "man_sheet.png"
        for i in range(0, 3):
            self.sprite_sheets["man{0}.png".format(i)] = (sheet_file_name, (i * 13, 0, 13, 10))

        sheet_file_name = "token.png"
        for i in range(0, 5):
            self.sprite_sheets["token{0}.png".format(i)] = (sheet_file_name, (i * 8, 0, 8, 8))

        sheet_file_name = "ladders_sheet.png"
        for i in range(0, 5):
            self.sprite_sheets["ladder{0}.png".format(i)] = (sheet_file_name, (0, i * 32, 32, 32))

        sheet_file_name = "switches_sheet.png"
        for i in range(0, 6):
            self.sprite_sheets["switch{0}.png".format(i)] = (sheet_file_name, (i * 32, 0, 32, 32))

        sheet_file_name = "doors_sheet.png"
        for i in range(0, 4):
            self.sprite_sheets["door{0}.png".format(i)] = (sheet_file_name, (i * 32, 0, 32, 32))

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

        sheet_file_name = "winter_sheet2.png"
        for i in range(0, 5):
            self.sprite_sheets["winter_tiles{0}.png".format(i)] = (sheet_file_name, (i * 119, 1, 96, 96))


class View():
    image_manager = ImageManager()

    def __init__(self, width: int = 0, height: int = 0):
        self.tick_count = 0
        self.height = height
        self.width = width
        self.surface = None

        View.image_manager.initialise()

    def initialise(self):
        pass

    def tick(self):
        self.tick_count += 1

    def process_event(self, new_event: model.Event):
        print("Default View Class event process:{0}".format(new_event))

    def draw(self):
        pass


class DWMainFrame(View):
    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    def __init__(self, model: model.DWModel):

        self.model = model
        self.surface = None
        self.width = 700
        self.height = 700

        # Create a view for rendering the model of the current world
        # Define how far away the camera is allowed to follow the player by setting min and max positions
        self.world_view = DWWorldView(self.model, min_view_pos=(200, -200, -350), max_view_pos=(800, 800, 400))
        self.inventory_view = DWInventoryView(self.model)
        self.text_box = DWTextBox("Hello World")

    def initialise(self):

        super(DWMainFrame, self).initialise()

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

    def print(self):

        print("Printing Dark Work view...")
        self.world_view.print()
        self.inventory_view.print()
        self.text_box.print()

    def inventory_show(self, view_on = None):
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

        x = 10
        y = 20

        # If the text box is active then draw it
        if self.text_box.is_visible is True:
            self.text_box.draw()
            self.surface.blit(self.text_box.surface, (x, y))

        x = 400
        y = 20

        # If the Inventory view is active then draw it
        if self.inventory_view.is_visible is True:
            self.inventory_view.draw()
            self.surface.blit(self.inventory_view.surface, (x, y))

        # Draw the number of remaining lives
        img = View.image_manager.get_skin_image(tile_name=model.Objects.PLAYER)
        for i in range(0, self.model.player_lives):
            self.surface.blit(img, (i * 32 + 8, self.world_view.surface.get_rect().height - 32))

        # Draw the game state is we are not playing
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
                             Colours.WHITE,
                             msg_rect,
                             2)

            draw_text(surface=self.surface,
                      msg="{0}".format(self.model.state),
                      x=self.world_view.width / 2,
                      y=self.world_view.height / 2,
                      size=32,
                      centre=True,
                      fg_colour=Colours.WHITE,
                      bg_colour=Colours.DARK_GREY)

    def update(self):
        pygame.display.update()

    def end(self):
        pygame.quit()

    def tick(self):
        self.world_view.tick()
        self.text_box.tick()

    def process_event(self, new_event: model.Event):
        self.world_view.process_event(new_event)
        self.text_box.process_event(new_event)

    def move_view(self, direction):
        self.world_view.move_view(direction)


class DWWorldView(View):

    def __init__(self, model: model.DWModel, min_view_pos, max_view_pos, view_pos=None):

        super(DWWorldView, self).__init__()

        # Connect to the model
        self.model = model

        self.surface = None

        # Multiplication factor for size of images
        self.object_size_scale = 1.0

        #  How big a view are we going to render?
        self.width = 600 * self.object_size_scale
        self.height = 600 * self.object_size_scale

        # How far away from the camera are we rendering objects before they disappear?
        self.depth = 60

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

        # Get what skin we are using for the world that we are drawing
        self.skin = self.model.world.skin

        self.surface.fill(Colours.BLACK)

        # Find out where the player currently is
        vx, vy, vz = self.model.world.get_player_xyz()
        pz = vz

        # Move the camera relative to the players position
        vz += self.camera_distance

        # Set the view at the position
        self.set_view((vx, vy, vz))

        # Get the visible objects at this view point from the model
        objs = self.m2v.get_object_list(self.view_pos,
                                        self.width * self.object_size_scale,
                                        self.height * self.object_size_scale,
                                        self.depth)

        # Draw visible objects in reverse order by distance from the camera
        distance = sorted(list(objs.keys()), reverse=True)

        # For each plane away from the camera...
        for d in distance:

            objs_at_d = objs[d]

            # For each object found in that plane...
            for pos, obj in objs_at_d:

                if obj.is_switch is True:
                    tick_count = obj.state
                elif obj.name in (model.Objects.PLAYER):
                    tick_count = obj.tick_count // 10
                else:
                    tick_count = self.tick_count

                # Get the image for the object based on the object's name
                image = View.image_manager.get_skin_image(obj.name,
                                                          skin_name=self.skin,
                                                          tick=tick_count)

                # If we got an image...
                if image is not None:
                    # Get the object's position in the view
                    x, y, z = pos

                    # Scale the object based on the size of the object and how far away from the camera it is
                    # Size adjust = 1 on the plane that the player is currently on
                    size_adj = (1 - (d + self.camera_distance) / self.infinity) * self.object_size_scale
                    size_w = int(obj.rect.width * size_adj)
                    size_h = int(obj.rect.height * size_adj)
                    image = pygame.transform.scale(image, (size_w, size_h))

                    # Change the image's transparency based on how far away from the player's plane it is
                    # Player's plane = opaque (alpha = 255)
                    # Between player and camera - increasing transparency the closer to the camera you get
                    # Beyond the player's plane - increasing levels of transparency
                    # alpha = 255 * (1 - min((abs(pz-d-vz)*20/self.m2v.infinity, 1)))
                    alpha = 255 * (1 - min((abs(pz - d - vz) / self.depth, 1)))
                    image.set_alpha(alpha)

                    # Blit the object image at the appropriate place and size
                    self.surface.blit(image, (
                        int(x * self.object_size_scale), int(y * self.object_size_scale), size_w, size_h))

        # Draw current view position
        msg = "View Pos={0} : Distances={1} : Tick={2}".format(self.view_pos, str(distance), self.tick_count)
        text_rect = (0, 0, 300, 30)
        drawText(surface=self.surface,
                 text=msg,
                 color=Colours.GOLD,
                 rect=text_rect,
                 font=pygame.font.SysFont(pygame.font.get_default_font(), 12),
                 bkg=Colours.DARK_GREY)

        msg = "  {0}  ".format(self.model.world.name)
        draw_text(surface=self.surface, msg=msg, x=self.width / 2, y=20, size=32, fg_colour=Colours.WHITE,
                  bg_colour=Colours.BLACK)

    def set_view(self, new_view_pos):
        # Set the position of the camera applying the minimum and maximum constraints of where is is allowed to go
        self.view_pos = np.clip(new_view_pos, self.min_view_pos, self.max_view_pos)

    def move_view(self, direction):
        new_view_pos = np.add(self.view_pos, direction)
        self.view_pos = np.clip(new_view_pos, self.min_view_pos, self.max_view_pos)


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
            # objects_at_z = self.model.world.planes[z].sort(key=lambda obj: obj.rect.y * 1000 + obj.rect.x)
            objects_at_z = self.model.world.planes[z]

            # For each object in the list...
            for obj in objects_at_z:

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


class DWTextBox(View):

    def __init__(self, model: str):
        super(DWTextBox, self).__init__()

        # Connect to the model
        self.model = model
        self.surface = None

        # Properties of the text box
        self.width = 100
        self.height = 150
        self.margin = 4
        self.padding = 4
        self.skin = "default"
        self.fg = Colours.WHITE
        self.bg = Colours.BLACK
        self.timer = self.tick_count
        self.life_time_ticks = 20

    @property
    def is_visible(self):
        return self.tick_count < (self.timer + self.life_time_ticks)

    def initialise(self):
        super(DWTextBox, self).initialise()

        print("Initialising {0}".format(__class__))
        self.surface = pygame.Surface((self.width, self.height))

        self.border_rect = (self.padding,
                            self.padding,
                            self.width - 2 * self.padding,
                            self.height - 2 * self.padding)

        self.text_rect = (self.padding + self.margin,
                          self.padding + self.margin,
                          self.width - 2 * (self.padding + self.margin),
                          self.height - 2 * (self.padding + self.padding))

    def print(self):
        print("Printing Dark Work Text Box view...")

    def process_event(self, new_event: model.Event):
        self.model = new_event.description
        self.timer = self.tick_count

    def draw(self):
        if self.tick_count > (self.timer + self.life_time_ticks):
            return

        self.surface.fill(Colours.DARK_GREY)

        pygame.draw.rect(self.surface,
                         Colours.WHITE,
                         self.border_rect,
                         2)

        text = drawText(surface=self.surface,
                        text=self.model,
                        rect=self.text_rect,
                        font=pygame.font.SysFont(pygame.font.get_default_font(), 16),
                        color=self.fg,
                        bkg=self.bg)

        # print("didn't blit {0}".format(text))


class DWInventoryView(View):

    def __init__(self, model: model.DWModel):
        super(DWInventoryView, self).__init__()

        # Connect to the model
        self.model = model
        self.surface = None

        # Properties of the text box
        self.width = 100
        self.height = 150
        self.margin = 4
        self.padding = 4
        self.skin = "default"
        self.fg = Colours.WHITE
        self.bg = Colours.BLACK
        self.timer = self.tick_count
        self.life_time_ticks = 20
        self.is_visible = False

    def initialise(self):
        super(DWInventoryView, self).initialise()

        print("Initialising {0}".format(__class__))
        self.surface = pygame.Surface((self.width, self.height))

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

    def process_event(self, new_event: model.Event):
        self.model = new_event.description
        self.timer = self.tick_count

    def draw(self):

        self.surface.fill(Colours.DARK_GREY)

        if self.is_visible is False:
            return

        # Get what skin we are using for the world that we are drawing
        self.skin = self.model.world.skin

        pygame.draw.rect(self.surface,
                         Colours.WHITE,
                         self.border_rect,
                         2)

        x = self.text_rect.centerx
        y = self.text_rect.y + 8
        size = 14
        icon_size = 20

        text = "Inventory:"
        draw_text(surface=self.surface, msg=text, x=x, y=y, size=18,
                  fg_colour=Colours.WHITE, bg_colour=Colours.DARK_GREY, centre=True)

        x = self.text_rect.x + 20

        for item, count in self.model.inventory.items():

            y += size + 1

            img = View.image_manager.get_skin_image(tile_name=item, skin_name=self.skin)
            img = pygame.transform.scale(img, (icon_size,icon_size))
            self.surface.blit(img, (self.text_rect.x, y-8))

            text = "{0} ({1})".format(item, count)
            draw_text(surface=self.surface, msg=text, x=x, y=y, size=size,
                      fg_colour=Colours.WHITE, bg_colour=Colours.DARK_GREY, centre=False)


