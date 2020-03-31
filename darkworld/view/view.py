import darkworld.model as model
from .graphics import *
import pygame
import os
import numpy as np
import logging

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
    initialised = False

    def __init__(self):
        pass

    def initialise(self):
        if ImageManager.initialised is False:
            self.load_skins()

    def get_image(self, image_file_name: str, width: int = 32, height: int = 32):

        if image_file_name not in ImageManager.image_cache.keys():

            filename = ImageManager.RESOURCES_DIR + image_file_name
            try:
                logging.info("Loading image {0}...".format(filename))
                #original_image = pygame.image.load(filename).convert_alpha()
                image = pygame.image.load(filename).convert()
                #image = pygame.transform.scale(original_image, (width, height))
                ImageManager.image_cache[image_file_name] = image
                logging.info("Image {0} loaded and cached.".format(filename))
                print("loading img")

            except Exception as err:
                print(str(err))

        return self.image_cache[image_file_name]

    def load_skins(self):

        new_skin_name = ImageManager.DEFAULT_SKIN
        new_skin = (new_skin_name, {

            model.Objects.WALL: "wall.png",
            model.Objects.PLAYER: ("bot.png", "bot.png"),
            model.Objects.TREASURE: "treasure.png",
            model.Objects.TREASURE_CHEST: "treasure_chest2.png",
            model.Objects.TRAP: "trap.png",
            model.Objects.KEY: "key2.png",
            model.Objects.BOSS_KEY: "boss_key.png",
            model.Objects.TILE1: "tile1.png",
            model.Objects.TILE2: "tile2.png",
            model.Objects.TILE3: "tile3.png",
            model.Objects.TELEPORT: "teleport2.png",
            model.Objects.HOLE: "down shoot.png",
            model.Objects.EXIT_NEXT: "exit.png",
            model.Objects.EXIT_PREVIOUS: "exit.png",


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


    def __init__(self, model : model.DWModel):

        self.model = model
        self.surface = None
        self.width = 800
        self.height = 800

        self.floor_view = DWFloorView(self.model, (0,0,-350), (2000,2000,500))


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

        self.floor_view.initialise()

    def print(self):

        print("Printing Dark Work view...")
        self.floor_view.print()

    def draw(self):

        self.surface.fill((255,0,255))

        pane_rect = self.surface.get_rect()

        x = 0
        y = 20

        self.floor_view.draw()
        self.surface.blit(self.floor_view.surface, (x, y))

    def update(self):
        pygame.display.update()

    def end(self):
        pygame.quit()

    def tick(self):
        self.floor_view.tick()

    def move_view(self, direction):

        self.floor_view.move_view(direction)


class DWFloorView(View):

    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    def __init__(self, model : model.DWModel, min_view_pos, max_view_pos, view_pos = None):

        super(DWFloorView, self).__init__()

        self.model = model
        self.surface = None
        self.width = 800
        self.height = 800
        self.depth = 400

        self.view_padding = 0

        self.max_view_pos = np.array(max_view_pos)
        self.min_view_pos = np.array(min_view_pos)
        if view_pos is None:
            view_pos = np.add(self.min_view_pos, self.max_view_pos)
            view_pos = np.divide(view_pos, 2).astype(int)
        self.set_view(view_pos)

        #self.object_size_scale = int(min(self.width, self.height)/100)
        self.object_size_scale = 1

        self.m2v = ModelToView3D(self.model)
        self.object_distance_scale = self.m2v.infinity

    def initialise(self):

        super(DWFloorView, self).initialise()

        print("Initialising {0}".format(__class__))
        self.surface = pygame.Surface((self.width, self.height))

    def print(self):

        print("Printing Dark Work Floor view...")
        print("View Pos = {0}\nPlayer pos = {1}".format(self.view_pos, self.model.world.player.xyz))
        vx, vy, vz = self.view_pos
        pz = self.model.world.player.z
        alpha = 255 * (1 - min((abs(pz - vx) * 10 / self.m2v.infinity, 1)))
        print("Alpha at vz={0},pz={1} = {2}".format(vz, pz, alpha))

        #objs = self.m2v.get_object_list(self.view_pos, self.width + (self.view_padding * 2), self.height + (self.view_padding * 2), self.depth)
        objs = self.m2v.get_object_list(self.view_pos, self.width, self.height, self.depth)

        # Draw visible objects in reverse order by distance
        distance = sorted(list(objs.keys()), reverse=True)

        for d in distance:
            alpha = 255 * (1 - min((abs(pz - d - vz) * 3 / self.m2v.infinity, 1)))
            print("Alpha at d={0},pz={1} = {2}".format(d, pz, alpha))

    def draw(self):

        self.surface.fill(Colours.BLACK)

        vx,vy,vz = self.model.world.get_player_xyz()
        pz = vz
        vz -= 28

        self.set_view((vx,vy,vz))

        # Get the visible objects from the model
        objs = self.m2v.get_object_list(self.view_pos, self.width, self.height, self.depth)

        # Draw visible objects in reverse order by distance
        distance = sorted(list(objs.keys()), reverse=True)
        for d in distance:
            objs_at_d = objs[d]
            for pos, obj in objs_at_d:

                x, y, z = pos

                size = int(obj.rect.width * self.object_size_scale * (1 - d / self.object_distance_scale))

                #image = self.tiles[min(obj.type, len(self.tiles)-1)]

                image = View.image_manager.get_skin_image(obj.name,
                                                          tick=self.tick_count)

                image = pygame.transform.scale(image ,(size, size))

                alpha = 255 * (1 - min((abs(pz-d-vz)*20/self.m2v.infinity, 1)))
                image.set_alpha(alpha)


                #self.surface.blit(image, (int(x * self.object_size_scale - size / 2), int(y * self.object_size_scale - size / 2), size, size))
                self.surface.blit(image, (int(x * self.object_size_scale), int(y * self.object_size_scale), size, size))

        # Draw cross hair
        cross_hair_size = 0.15
        #pygame.draw.circle(self.surface, Colours.WHITE, (int(self.width / 2), int(self.height / 2)), 10, 1)
        # pw = self.model.world.player.rect.width/2
        # ph = self.model.world.player.rect.height/2
        # pygame.draw.rect(self.surface,
        #                  Colours.GOLD,
        #                  (int(self.width / 2 * (1 - cross_hair_size) + pw),
        #                   int(self.height / 2 * (1 - cross_hair_size) + ph),
        #                   int(self.width * cross_hair_size),
        #                   int(self.height * cross_hair_size)),
        #                  2)

        # Draw current view position
        msg = "View Pos={0} : Distances={1}".format(self.view_pos, str(distance))
        text_rect = (0, 0, 300, 30)
        drawText(surface=self.surface,
                 text=msg,
                 color=Colours.GOLD,
                 rect=text_rect,
                 font=pygame.font.SysFont(pygame.font.get_default_font(), 12),
                 bkg=Colours.DARK_GREY)

    def tick(self):

        return

    def set_view(self, new_view_pos):
        self.view_pos = np.clip(new_view_pos, self.min_view_pos, self.max_view_pos)

    def move_view(self, direction):

        new_view_pos = np.add(self.view_pos, direction)
        self.view_pos = np.clip(new_view_pos, self.min_view_pos, self.max_view_pos)


class ModelToView3D():

    PERSPECTIVE = "perspective"
    PARALLEL = "parallel"

    def __init__(self, model):
        self.model = model

        self.infinity = 2000

        self.projection = ModelToView3D.PERSPECTIVE

    def get_object_list(self, view_pos, view_width, view_height, view_depth):

        objects = {}

        vx, vy, vz = view_pos

        for z in self.model.world.planes.keys():

            objects_at_z = self.model.world.planes[z]

            for obj in objects_at_z:

                ox,oy,oz = obj.xyz

                # Calculate where the object is versus the current view point
                od = oz - vz
                ow = ox - vx
                oh = oy - vy

                # filter out objects that don't fit into the current view.
                if od <= 0 or od > view_depth or abs(ow) > view_width / 2 or abs(oh) > view_height / 2:
                    pass
                else:

                    # If we don't have a list of objects at this distance then create an empty one
                    if od not in objects.keys():
                        objects[od] = []

                    # Add ((x,y,z), obj)) to list of objects at this distance where x,y,x is the adjusted view position
                    objects[od].append((
                        (int(ow * (1 - od / self.infinity * (self.projection == ModelToView3D.PERSPECTIVE))) + int(view_width / 2),
                         int(oh * (1 - od / self.infinity * (self.projection == ModelToView3D.PERSPECTIVE))) + int(view_height / 2),
                         od), obj))

        return objects

