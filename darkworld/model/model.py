import collections
import os

from darkworld.model.worlds import *

class DWModel():

    DATA_FILES_DIR = os.path.dirname(__file__) + "\\data\\"

    def __init__(self, name: str):
        self.name = name
        self.tick_count = 0
        self.events = EventQueue()

        self.world_factory = None
        self.world = None
        self.current_world_id = -1

        self.player = None
        self.inventory = {}

    def initialise(self):
        print("Initialising {0}:{1}".format(self.name, __class__))

        self.world_factory = WorldBuilder(DWModel.DATA_FILES_DIR)
        self.world_factory.initialise()
        self.world = self.world_factory.get_world(self.current_world_id)

        size = 32

        self.player = RPGObject3D(type=7,
                                  name=Objects.PLAYER,
                                  opos=(size * 9, size * 9, 1),
                                  osize=(size, size, 1))

        self.move_world(1)

    def print(self):
        print("Printing {0} model...".format(self.name))
        print("Player currently at {0}".format(self.player.xyz))
        for obj, count in self.inventory.items():
            print("Carrying {0} x {1}".format(obj,count))
        self.world.print()


    def process_event(self, new_event):
        print("Default Game event process:{0}".format(new_event))

    def tick(self):
        self.tick_count += 1
        self.world.move_player(World3D.NORTH)
        if self.world.player.has_changed_planes() is True:
            self.world.state = World3D.PLAYER_FALLING
        else:
            self.world.state = World3D.PLAYER_MOVING

    def get_next_event(self):
        next_event = None
        if self.events.size() > 0:
            next_event = self.events.pop_event()

        return next_event

    def move_player(self, vector):

        if self.world.state == World3D.PLAYER_FALLING:
            return

        self.world.move_player(vector)

        touching_objects = self.world.touching_objects(self.world.player)

        for object in touching_objects:

            if object.name == Objects.EXIT_NEXT:
                req_obj = Objects.BOSS_KEY
                if self.world.player.is_inside(object):
                    if self.have_object(req_obj) is True:
                        print("Using {0} to go to next world...".format(req_obj))
                        if self.move_world(self.current_world_id + 1) is True:
                            self.use_object(req_obj)
                            print(str(self.world))
                    else:
                        print("You don't have required object {0}".format(req_obj))

            elif object.name == Objects.EXIT_PREVIOUS:
                if self.world.player.is_inside(object):
                    print("Going back to previous world...")
                    if self.move_world(self.current_world_id - 1) is True:
                        self.use_object(Objects.BOSS_KEY, count=-1)
                        print(str(self.world))

            elif object.name == Objects.HOLE:
                print("Falling...")
                self.move_player((0,0,-2))

            elif object.name == Objects.TRAP:
                if self.world.player.is_colliding(object):
                    print("Ouch...")
                    self.world.delete_object3D(object)


    def interact(self):

        touching_objects = self.world.touching_objects(self.world.player)

        for object in touching_objects:
            if object.is_interactable is True:

                print("Interacting with {0}".format(str(object)))

                if object.name == Objects.TELEPORT:
                    if self.world.player.is_inside(object):
                        print("Teleporting...")
                        self.world.move_player_to_start()

                elif object.name == Objects.TREASURE_CHEST:
                    req_obj = Objects.KEY
                    if self.have_object(req_obj) is True:
                        print("Using {0} to open chest...".format(req_obj))
                        self.use_object(req_obj)
                        self.swap_object(object, Objects.TREASURE)

                    else:
                        print("You don't have required object {0}".format(req_obj))
                else:
                    self.collect_object(object)
                    self.world.delete_object3D(object)


    def collect_object(self, new_object):
        if new_object.is_collectable is True:
            if new_object.name not in self.inventory.keys():
                self.inventory[new_object.name] = 0
            self.inventory[new_object.name] += 1

    def have_object(self, object_name : str):
        have = False

        if object_name in self.inventory.keys() and self.inventory[object_name] > 0:
            have = True

        return have

    def use_object(self, object_name : str, count = 1):
        if object_name in self.inventory.keys():
                self.inventory[object_name] -= count

    def swap_object(self, old_object, new_object_name):

        xyz = old_object.xyz
        new_object = WorldObjectLoader.get_object_copy_by_name(new_object_name)
        new_object.set_pos(xyz)
        self.world.add_object3D(new_object)
        self.world.delete_object3D(old_object)

    def move_world(self, new_world_id : int):

        moved = False

        print("Moving from world {0} to world {1}".format(self.current_world_id, new_world_id))

        if self.current_world_id == new_world_id:
            return

        new_world = self.world_factory.get_world(new_world_id)

        if new_world is not None:

            if self.world is not None:
                self.world.delete_player()

            self.world = new_world
            self.world.add_player(self.player, start_pos = (self.current_world_id < new_world_id))
            self.current_world_id = new_world_id
            moved = True
        else:
            print("Can't find new world {0}".format(new_world_id))

        return moved


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

