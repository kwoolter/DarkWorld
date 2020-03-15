import collections
import copy
import random
import numpy as np

class DWModel():

    def __init__(self, name : str):

        self.name = name
        self.tick_count = 0

        self.events = EventQueue()

        self.world = World3D(w = 1000, h = 1000, d = 20)

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

    def initialise(self, obj_count=500):

        for i in range(1, obj_count):
            new_object = Object3D(random.randint(0, 5),
                                  random.randint(1, 5),
                                  random.choice(World3D.HEADINGS))

            self.add_object(new_object, random.randint(0, self.width), random.randint(0, self.height),
                            random.randint(0, self.depth))


        for i in range(30, 100):
            new_object = Object3D(int((i % 10) / 2), 10, random.choice(World3D.HEADINGS))

            self.add_object(new_object, 300 + i * 20, 300, 10)
            self.add_object(new_object, 700, 700 + i * 20, 10)


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
