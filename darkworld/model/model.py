import collections
import copy
import random
import numpy as np
import logging
import pygame

class DWModel():

    def __init__(self, name : str):

        self.name = name
        self.tick_count = 0

        self.events = EventQueue()

        self.world = World3D(w = 1000, h = 1000, d = 1000)

    def initialise(self):

        print("Initialising {0}:{1}".format(self.name, __class__))

        self.world.initialise()


    def print(self):
        print("Printing {0} model...".format(self.name))

    def process_event(self, new_event):
        print("Default Game event process:{0}".format(new_event))

    def tick(self):

        self.tick_count += 1

    def get_next_event(self):

        next_event = None
        if self.events.size() > 0:
            next_event = self.events.pop_event()

        return next_event

    def end(self):
        pass

class Event():
    # Event Types
    QUIT = "quit"
    DEFAULT = "default"
    STATE = "state"
    GAME = "game"
    FLOOR = "floor"
    BATTLE = "battle"

    # Events
    TICK = "Tick"
    PLAYING = "playing"
    COLLIDE = "collide"
    INTERACT = "interact"
    BLOCKED = "blocked"
    SECRET = "secret"
    TREASURE = "treasure"
    DOOR_OPEN = "door opened"
    DOOR_LOCKED = "door locked"
    SWITCH = "switch"
    FOUND_FLAG = "found_flag"
    KEY = "key"
    TELEPORT = "teleport"
    GAIN_HEALTH = "gain health"
    LOSE_HEALTH = "lose health"
    NO_AP = "No action points"
    KILLED_OPPONENT = "killed opponent"
    MISSED_OPPONENT = "missed opponent"
    DAMAGE_OPPONENT = "damaged opponent"
    VICTORY = "victory"
    NEXT_PLAYER = "next player"

    def __init__(self, name: str, description: str = None, type: str = DEFAULT):
        self.name = name
        self.description = description
        self.type = type

    def __str__(self):
        return "{0}:{1} ({2})".format(self.name, self.description, self.type)


class EventQueue():
    def __init__(self):
        self.events = collections.deque()

    def add_event(self, new_event: Event):
        self.events.append(new_event)

    def pop_event(self):
        return self.events.pop()

    def size(self):
        return len(self.events)

    def print(self):
        for event in self.events:
            print(event)


class World3D:

    INVERSE = np.array([-1, -1, -1])
    NORTH = np.array([0, 0, 1])
    SOUTH = np.multiply(NORTH, INVERSE)
    EAST = np.array([1, 0, 0])
    WEST = np.multiply(EAST, INVERSE)
    UP = np.array([0, 1, 0])
    DOWN = np.multiply(UP, INVERSE)

    HEADINGS = (NORTH, SOUTH, EAST, WEST, UP, DOWN)

    def __init__(self, w, h, d):

        self.width = w
        self.height = h
        self.depth = d

        self.objects = []

    def add_object(self, new_object, x, y, z):

        if self.is_valid_xyz(x, y, z) is True:
            self.objects.append(((x, y, z), copy.deepcopy(new_object)))

    def is_valid_xyz(self, x, y, z):

        if x < 0 or x > self.width or y < 0 or y > self.height or z < 0 or z > self.depth:
            return False
        else:
            return True


    def is_collision(self, a , b):

        hit = False


        return hit

    def initialise(self, obj_count=500):

        # Change to scale the size of each object in the world
        obj_size = 32

        layer2_distance = 500

        new_object = Object3D(2, obj_size)
        for i in range(1, 10):

            self.add_object(new_object,
                            random.randint(1, 10) * obj_size,
                            random.randint(1, 10) * obj_size,
                            19)


            self.add_object(new_object,
                            (random.randint(1, 10) + 10) * obj_size,
                            (random.randint(1, 10) + 5) * obj_size,
                            layer2_distance - 1)

        new_object = Object3D(3, obj_size * 2)
        for i in range(1, 10):

            self.add_object(new_object,
                            random.randint(1, 10) * obj_size,
                            random.randint(1, 10) * obj_size,
                            10)

        new_object1 = Object3D(1, obj_size, random.choice(World3D.HEADINGS))
        new_object2 = Object3D(4, obj_size, random.choice(World3D.HEADINGS))
        for y in range(0,15):
            for x in range(0, 15):


                self.add_object(new_object2, (x + 10)*obj_size, (y+5)*obj_size, layer2_distance)
                self.add_object(new_object2, x * obj_size, (y + 5) * obj_size, layer2_distance)

                self.add_object(new_object1, x*obj_size, y*obj_size, 20)



        new_object = Object3D(0, obj_size, random.choice(World3D.HEADINGS))
        for y in range(0,30):
            self.add_object(new_object, 0, y * obj_size, 19)
            self.add_object(new_object, 12 * obj_size, y * obj_size, 19)

        new_object = Object3D(0, obj_size, random.choice(World3D.HEADINGS))
        for x in range(0,30):
            self.add_object(new_object, x * obj_size, 0,  19)
            self.add_object(new_object, x * obj_size, 12 * obj_size, 19)



    def print(self):
        print("Headings {0}".format(World3D.HEADINGS))
        for pos, obj in self.objects:
            print("{0}:{1}".format(pos, obj))


class Object3D:

    def __init__(self, type, size=1, facing=World3D.NORTH):
        self.type = type
        self.size = size
        self.facing = facing

    def __str__(self):
        return "type({0})".format(self.type)


class RPGObject3D(object):

    TOUCH_FIELD_X = 3
    TOUCH_FIELD_Y = 3

    def __init__(self, name: str,
                 opos,
                 osize,
                 solid: bool = True,
                 visible: bool = True,
                 interactable: bool = True):

        self.name = name

        # Position and size
        ox,oy,oz = opos
        ow,oh,od = osize
        self._rect = pygame.Rect(ox,oy, ow, oh)
        self._z = oz

        self._old_rect = self._rect.copy()

        # Properties
        self.is_solid = solid
        self.is_visible = visible
        self.is_interactable = interactable

        # Movement
        self.dx = 0
        self.dy = 0
        self.d2x = 0
        self.d2y = 0

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, new_rect):
        self._old_rect = self._rect.copy()
        self._rect = new_rect

    @property
    def z(self):
        return self._z

    @rect.setter
    def z(self, new_z):
        self._old_z = self.z
        self._z = new_z

    def back(self):
        logging.info("Moving Object {0} back from {1} to {2}".format(self.name, self._rect, self._old_rect))
        self._rect = self._old_rect.copy()

    def is_colliding(self, other_object):
        return self.z == other_object.layer and \
               self != other_object and \
               self.rect.colliderect(other_object.rect)

    def is_touching(self, other_object):

        touch_field = self._rect.inflate(RPGObject3D.TOUCH_FIELD_X, RPGObject3D.TOUCH_FIELD_Y)

        return self.z == other_object.layer and \
               self.is_visible and \
               self.is_interactable and \
               self != other_object and \
               touch_field.colliderect(other_object.rect)

    def move(self, dx: int, dy: int):
        self._old_rect = self._rect.copy()
        self.rect.x += dx
        self.rect.y += dy

    def set_pos(self, x: int, y: int, z : int = 0):
        self._old_rect = self._rect.copy()
        self.rect.x = x
        self.rect.y = y
        self.z = z

    def get_pos(self):
        return self._rect.x, self._rect.y, self.z