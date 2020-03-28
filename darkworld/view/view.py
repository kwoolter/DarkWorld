import darkworld.model as model

from .graphics import *

import pygame
import os
import numpy as np

class View():
    #image_manager = ImageManager()

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

        self.model = model
        self.surface = None
        self.width = 800
        self.height = 800
        self.depth = 1000

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

        self.tiles = []

        filenames = ("tile1.png", "tile3.png", "tile4.png", "bear.png", "tile2.png", "tile5.png", "tile6.png", "bot.png")

        try:
            for filename in filenames:
                filename = DWFloorView.RESOURCES_DIR + filename
                image = pygame.image.load(filename).convert()
                self.tiles.append(image)

        except Exception as err:
            print(str(err))

    def print(self):

        print("Printing Dark Work Floor view...")

    def draw(self):

        self.surface.fill(Colours.DARK_GREY)

        vx,vy,vz = self.model.world.get_player_xyz()

        vz -= 20

        self.view_pos = (vx,vy,vz)

        # Get the visible objects from the model
        #objs = self.m2v.get_object_list(self.view_pos, self.width + (self.view_padding * 2), self.height + (self.view_padding * 2), self.depth)
        #view_pos = np.add(self.view_pos, np.array((-1000,-1000,0)))
        objs = self.m2v.get_object_list(self.view_pos, self.width, self.height, self.depth)

        # Draw visible objects in reverse order by distance
        distance = sorted(list(objs.keys()), reverse=True)
        for d in distance:
            objs_at_d = objs[d]
            for pos, obj in objs_at_d:

                x, y, z = obj.xyz

                size = int(obj.rect.width * self.object_size_scale * (1 - d / self.object_distance_scale))

                image = self.tiles[min(obj.type, len(self.tiles)-1)]

                image = pygame.transform.scale(image ,(size, size))

                image.set_alpha(255 * (1 - min(d*2/self.m2v.infinity, 1)))

                #brighten = min(int(d), 255)
                #image.fill((brighten, brighten, brighten), special_flags=pygame.BLEND_RGB_ADD)

                # pygame.draw.rect(self.surface,
                #                  Colours.BLACK,
                #                  (int(x * self.object_size_scale - size / 2),
                #                  int(y * self.object_size_scale - size / 2),
                #                  size,
                #                  size),
                #                  0)

                self.surface.blit(image, (int(x * self.object_size_scale - size / 2), int(y * self.object_size_scale - size / 2), size, size))

        # Draw cross hair
        cross_hair_size = 0.25
        pygame.draw.circle(self.surface, Colours.WHITE, (int(self.width / 2), int(self.height / 2)), 10, 1)
        pygame.draw.rect(self.surface,
                         Colours.GOLD,
                         (int(self.width / 2 * (1 - cross_hair_size)),
                          int(self.height / 2 * (1 - cross_hair_size)), int(self.width * cross_hair_size),
                          int(self.height * cross_hair_size)),
                         2)

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

        pass

        #self.view_pos = np.add(self.view_pos, np.array(model.World3D.NORTH))

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

        self.infinity = 3000

        self.projection = ModelToView3D.PERSPECTIVE
        #self.projection = ModelToView3D.PARALLEL

    def get_object_list(self, view_pos, view_width, view_height, view_depth):

        objects = {}

        vx, vy, vz = view_pos

        for (ox, oy, oz), obj in self.model.world.objects:

            od = oz - vz
            ow = ox - vx
            oh = oy - vy
            #if od <= 0 or od > view_depth or abs(ow) > view_width / 2 or abs(oh) > view_height / 2:
            if od <= 0 or od > view_depth:
                pass
            else:

                # If we don't have a list of objects at this distance then create an empty one
                if od not in objects.keys():
                    objects[od] = []

                # Add ((x,y,z), obj)) to list of objects at this distance
                objects[od].append((
                    (int(ow * (1 - od / self.infinity * (self.projection == ModelToView3D.PERSPECTIVE))) + int(view_width / 2),
                     int(oh * (1 - od / self.infinity * (self.projection == ModelToView3D.PERSPECTIVE))) + int(view_height / 2),
                     od), obj))

        return objects