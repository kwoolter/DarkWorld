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

        self.world = World3D(w = 1500, h = 1500, d = 1000)

    def initialise(self):

        print("Initialising {0}:{1}".format(self.name, __class__))

        self.world.initialise()

        #new_player = RPGObject3D("Keith", (300,300,0), (32,32,1))
        size = 64
        new_player = RPGObject3D(type=7,
                                 name="Player",
                                 opos=(300, 300, 10),
                                 osize=(size, size, 1))

        self.world.add_player(new_player)


    def print(self):
        print("Printing {0} model...".format(self.name))

        self.world.print()

        # objs = self.world.get_objects_at(self.player.xyz)
        # for obj in objs:
        #     print(str(obj))

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

        self.planes = {}

    @property
    def rect(self):
        return pygame.Rect(0,0,self.width,self.height)

    def add_object(self, new_object, x, y, z):

        if self.is_valid_xyz(x, y, z) is True:
            copy_of_new_object = copy.deepcopy(new_object)
            self.objects.append(((x, y, z), copy_of_new_object))

            if z not in self.planes.keys():
                self.planes[z] = {}

            self.planes[z][(x, y)] = new_object

        else:
            print("Can't add obje3ct {0} at ({1},{2},{3})".format(str(new_object),x,y,z))

    def add_object3D(self, new_object, do_copy : bool = True):

        x,y,z = new_object.xyz

        if self.is_valid_xyz(x, y, z) is True:

            if do_copy is True:
                new_object = copy.deepcopy(new_object)

            if z not in self.planes.keys():
                self.planes[z] = []

            self.planes[z].append(new_object)

        else:
            print("Can't add object {0} at ({1},{2},{3})".format(str(new_object),x,y,z))

    def delete_object3D(self, selected_object, plane : int = None):

        x,y,z = selected_object.xyz

        if plane is not None:
            z = plane

        if z in self.planes.keys():
            self.planes[z].remove(selected_object)
        else:
            print("Can't delete object {0} at ({1},{2},{3})".format(str(selected_object),x,y,z))

    def add_player(self, new_player):

        self.player = new_player

        self.add_object3D(new_player, do_copy = False)

        return

    def is_valid_xyz(self, x, y, z):

        if x < 0 or x > int(self.width) or y < 0 or y > int(self.height) or z < 0 or z > int(self.depth):
            return False
        else:
            return True


    def initialise(self):

        # Set the scale of each object in the world
        obj_size = 32
        layer2_distance = 800

        for i in range(1, 10):
            z = 19
            new_object = RPGObject3D(type=2,
                                     name="Object {0}:{1}".format(type, i),
                                     opos=(random.randint(1, 10) * obj_size,
                                           random.randint(1, 10) * obj_size,
                                           z),
                                     osize=(obj_size, obj_size, 1))

            self.add_object3D(new_object)

            z = layer2_distance
            new_object = RPGObject3D(type=3,
                                     name="Object {0}:{1}".format(type, i),
                                     opos=((random.randint(1, 10) + 10) * obj_size,
                                           (random.randint(1, 10) + 10) * obj_size,
                                           z - 1),
                                     osize=(obj_size, obj_size, 1))

            self.add_object3D(new_object)

        # new_object = Object3D(3, obj_size * 2)
        # for i in range(1, 10):
        #
        #     self.add_object(new_object,
        #                     random.randint(1, 10) * obj_size,
        #                     random.randint(1, 10) * obj_size,
        #                     10)
        #
        # new_object = Object3D(6, obj_size)
        # for i in range(1, 15):
        #
        #     self.add_object(new_object,
        #                     (random.randint(0, 10) + 20) * obj_size,
        #                     (random.randint(0, 10) + 10) * obj_size,
        #                     int(layer2_distance / 2)-1)
        #


        # Create some floors
        new_object1 = Object3D(1, obj_size, random.choice(World3D.HEADINGS))
        new_object2 = Object3D(5, obj_size, random.choice(World3D.HEADINGS))
        for y in range(0,15):
            for x in range(0, 15):
                obj_size = 32
                z = 19
                otype = 1
                new_object = RPGObject3D(type=otype,
                                         name="Object {0}:{1},{2}".format(otype, x, y),
                                         opos=(x * obj_size,
                                               y * obj_size,
                                               z),
                                         osize=(obj_size, obj_size, 1))
                self.add_object3D(new_object)
                z = layer2_distance
                new_object = RPGObject3D(type=otype,
                                         name="Object {0}:{1},{2}".format(otype, x, y),
                                         opos=((x + 15) * obj_size,
                                               (y + 5) * obj_size,
                                                z),
                                         osize=(obj_size, obj_size, 1))

                self.add_object3D(new_object)

                # self.add_object(new_object2, (x + 15)*obj_size, (y+5)*obj_size, layer2_distance)
                # self.add_object(new_object2, (x + 20) * obj_size, (y + 10) * obj_size, int(layer2_distance / 2))
                # self.add_object(new_object2, x * obj_size, (y + 5) * obj_size, layer2_distance)
                #
                # self.add_object(new_object1, x*obj_size, y*obj_size, 20)
        #
        #
        # # Add vertical walls
        # new_object = Object3D(0, obj_size, random.choice(World3D.HEADINGS))
        # for y in range(0,30):
        #     self.add_object(new_object, 0, y * obj_size, 19)
        #     self.add_object(new_object, 12 * obj_size, y * obj_size, 19)
        #     self.add_object(new_object, 20 * obj_size, y * obj_size, 19)
        #
        # # Add horizontal walls
        # new_object = Object3D(0, obj_size, random.choice(World3D.HEADINGS))
        # for x in range(0,30):
        #     self.add_object(new_object, x * obj_size, 0,  19)
        #     self.add_object(new_object, x * obj_size, 12 * obj_size, 19)
        #     self.add_object(new_object, x * obj_size, 20 * obj_size, 19)


    def move_object_by(self, obj, vector):

        dx, dy, dz = vector

        if dx != 0:
            self.move_object(obj, (dx,0,0))

        if dy !=0:
            self.move_object(obj, (0,dy,0))

        if dz != 0:
            self.move_object(obj, (0,0,dz))


    def move_object(self, obj, vector):

        opos = obj.xyz
        vector = np.array(vector)
        new_opos = np.add(opos, vector)

        hit_objects = self.get_objects_at(new_opos)

        if len(hit_objects) == 0:
            obj.xyz = new_opos

    def move_player(self, vector):

        dx, dy, dz = vector

        selected_player = self.player

        #objects = self.get_objects_by_plane(selected_player.z + dz)
        new_plane = selected_player.z + dz
        if new_plane in self.planes.keys():
            objects = self.planes[new_plane]
        else:
            objects = []

        # Are we attempting to change planes?
        if dz != 0:
            selected_player.move(0, 0, dz)

            if self.rect.contains(selected_player.rect) is False:
                selected_player.back()
                print("DZ:Player {0} moving to {1} goes outside the world".format(self.player, vector))
            else:
                for object in objects:
                    if object.is_solid is True and object.is_colliding(selected_player):
                        selected_player.back()
                        print("DZ:Player {0} collided with object {1}".format(self.player, object))
                        break

        # If we succeeded in moving planes...
        if selected_player.has_changed_planes() is True:

            print("Player has changed planes from {0} to {1}".format(self.player.z, self.player._old_z))

            # Get the objects for the new plane
            new_plane = selected_player.z
            if new_plane in self.planes.keys():
                objects = self.planes[new_plane]
            else:
                objects = []

        # Are we attempting to change X position?
        if dx != 0:
            selected_player.move(dx, 0, 0)

            if self.rect.contains(selected_player.rect) is False:
                selected_player.back()
            else:
                for object in objects:
                    if object.is_solid is True and object.is_colliding(selected_player):
                        selected_player.back()
                        print("DX:Player {0} collided with object {1}".format(self.player, object))
                        break

        # Are we attempting to change Y position?
        if dy != 0:
            selected_player.move(0, dy, 0)

            if self.rect.contains(selected_player.rect) is False:
                selected_player.back()
            else:
                for object in objects:
                    if object.is_solid is True and object.is_colliding(selected_player):
                        selected_player.back()
                        print("DY:Player {0} collided with object {1}".format(self.player, object))
                        break

        # did we move anywhere?
        if self.player.has_moved() is True:
            print("Player moved from {0} to {1}".format(self.player.xyz, self.player.old_xyz))

            # If we succeeded in moving planes...
            if selected_player.has_changed_planes() is True:
                print("Player has changed planes from {0} to {1}".format(self.player.z, self.player._old_z))
                # Adjust the plane data to reflect new position
                self.delete_object3D(self.player, self.player._old_z)
                self.add_object3D(self.player, do_copy=False)


    def get_player_xyz(self):
        return self.player.xyz

    def get_objects_by_plane(self, z : int = None):

        objects_by_plane = []

        if z is None:
            plane_ids = sorted(self.planes.keys(), reverse=True)
        else:
            plane_ids = []
            if z in self.planes.keys():
                plane_ids.append(z)

        for plane_id in plane_ids:
            current_plane = self.planes[plane_id]
            for obj in current_plane:
                objects_by_plane.append(obj)


        return objects_by_plane


    def get_objects_at(self, x, y, z):

        matching_objects = []

        if z in self.planes.keys():

            for obj in self.planes[z].values():
                if self.is_collision((x,y,z), obj) is True:
                    matching_objects.append(obj)

        return matching_objects



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
                 type : int = 0,
                 opos = (0,0,0),
                 osize = (1,1,1),
                 solid: bool = True,
                 visible: bool = True,
                 interactable: bool = True):

        self.name = name
        self.type = type

        # Position and size
        ox,oy,oz = opos
        ow,oh,od = osize
        self._z = oz
        self._old_z = oz
        self._rect = pygame.Rect(ox,oy, ow, oh)
        self._old_rect = self._rect.copy()

        # Properties
        self.is_solid = solid
        self.is_visible = visible
        self.is_interactable = interactable

    def __str__(self):
        return "{0} ({1})".format(self.name, self.type)

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, new_rect):
        self._old_rect = self._rect.copy()
        self._rect = new_rect

    @property
    def xyz(self):
        return (int(self._rect.x), int(self._rect.y), int(self._z))

    @property
    def old_xyz(self):
        return (int(self._old_rect.x), int(self._old_rect.y), int(self._old_z))

    @property
    def z(self):
        return int(self._z)

    @z.setter
    def z(self, new_z):
        self._old_z = self._z
        self._z = int(new_z)

    def back(self):
        logging.info("Moving Object {0} back from {1} to {2}".format(self.name, self._rect, self._old_rect))
        self._rect = self._old_rect.copy()
        self._z = self._old_z

    def is_colliding(self, other_object):
        return self.z == other_object.z and \
               self != other_object and \
               self.rect.colliderect(other_object.rect)

    def is_touching(self, other_object):

        touch_field = self._rect.inflate(RPGObject3D.TOUCH_FIELD_X, RPGObject3D.TOUCH_FIELD_Y)

        return self.z == other_object.layer and \
               self.is_visible and \
               self.is_interactable and \
               self != other_object and \
               touch_field.colliderect(other_object.rect)

    def has_moved(self):
        return self._z != self._old_z or self._rect != self._old_rect

    def has_changed_planes(self):
        return int(self._z) != int(self._old_z)

    def move(self, dx: int, dy: int, dz : int):
        self._old_rect = self._rect.copy()
        self.rect.x += dx
        self.rect.y += dy
        self.z += dz

    def set_xyz(self, x: int, y: int, z : int = 0):
        self.set_pos((x,y,z))

    def get_xyz(self):
        return self.get_pos()

    def set_pos(self, new_pos):
        x, y, z = new_pos
        self._old_rect = self._rect.copy()
        self.rect.x = x
        self.rect.y = y
        self.z = z

    def get_pos(self):
        return (self._rect.x, self._rect.y, self._z)