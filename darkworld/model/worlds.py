import csv
import logging
import copy
import pygame
import numpy as np
import random
from .objects import Objects




class RPGObject3D(object):

    TOUCH_FIELD_X = 3
    TOUCH_FIELD_Y = 3

    def __init__(self, name: str,
                 type: int = 0,
                 opos=(0, 0, 0),
                 osize=(1, 1, 1),
                 solid: bool = True,
                 visible: bool = True,
                 interactable: bool = False,
                 collectable: bool = False,
                 switchable: bool = False,
                 state=None):

        self.name = name
        self.type = type
        self.state = state

        if switchable is True:
            self.state = False

        # Position and size
        ox, oy, oz = opos
        ow, oh, od = osize
        self._z = oz
        self._old_z = oz
        self._rect = pygame.Rect(ox, oy, ow, oh)
        self._old_rect = self._rect.copy()

        # Properties
        self.is_solid = solid
        self.is_visible = visible
        self.is_interactable = interactable
        self.is_collectable = collectable
        self.is_switchable = switchable

    def __str__(self):
        return "{0} type({1}) pos({2})".format(self.name, self.type, self.xyz)

    def get_current_object(self):
        return self

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

    def is_touching(self, other_object, distance = None):

        if distance is None:
            touch_field = self._rect.inflate(RPGObject3D.TOUCH_FIELD_X, RPGObject3D.TOUCH_FIELD_Y)
        else:
            touch_field = self._rect.inflate(int(distance), int(distance))

        return self.z == other_object.z and \
               self.is_visible and \
               self != other_object and \
               touch_field.colliderect(other_object.rect)

    def is_inside(self, other_object):
        # b = other_object.rect.contains(self.rect)
        # print("{0} contains {1} = {2}".format(other_object.name, self.name, b))

        return self.z == other_object.z and \
               self != other_object and \
               other_object.rect.contains(self.rect)

    def contains(self, other_object):
        return self.z == other_object.z and \
               self != other_object and \
               self.rect.contains(other_object.rect)

    def has_moved(self):
        return self._z != self._old_z or self._rect != self._old_rect

    def has_changed_planes(self):
        return int(self._z) != int(self._old_z)

    def move(self, dx: int, dy: int, dz: int):
        self._old_rect = self._rect.copy()
        self.rect.x += dx
        self.rect.y += dy
        self.z += dz

    def set_xyz(self, x: int, y: int, z: int = 0):
        self.set_pos((x, y, z))

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


class SwitchableObject(RPGObject3D):

    def __init__(self, a : RPGObject3D, b : RPGObject3D):
        self.switch_state = False
        self.switch_objects = [a, b]

    def switch(self, state : bool = None):
        if state is None:
            self.state = not self.state
        else:
            self.state = state

    def get_current_object(self):
        if self.state is False:
            return self.switch_objects[0]
        else:
            return self.switch_objects[1]


class SwitchGroup:
    AND = "and"
    OR = "or"

    def __init__(self, name: str, type=AND):

        self.name = name
        self.type = type
        self.switches = []

    def add_switch(self, new_switch):

        self.switches.append(new_switch)

    def add_switchable_object(self, new_object: SwitchableObject):
        pass

    def output(self):

        result = False
        or_result = False
        and_result = True

        for switch in self.switches:
            or_result = or_result or switch.state
            and_result = and_result and switch.state

        if self.type == SwitchGroup.AND:
            result = and_result

        elif self.type == SwitchGroup.OR:
            result = or_result

        return result

    def print(self):
        print("Switch group {0}: type=({1}), switches={2}, output={3}".format(self.name,
                                                                              self.type,
                                                                              len(self.switches),
                                                                              self.output()))


class WorldBuilder():
    FLOOR_LAYOUT_FILE_NAME = "_floor_layouts.csv"
    FLOOR_OBJECT_FILE_NAME = "_floor_objects.csv"

    def __init__(self, data_file_directory: str):
        self.data_file_directory = data_file_directory
        self.world_properties = {}

        self.world_layouts = None
        self.world_objects = None

    def initialise(self, file_prefix: str = "default"):

        self.world_objects = WorldObjectLoader(
            self.data_file_directory + file_prefix + WorldBuilder.FLOOR_OBJECT_FILE_NAME)
        self.world_objects.load()
        self.world_objects.print()

        self.world_layouts = WorldLayoutLoader(
            self.data_file_directory + file_prefix + WorldBuilder.FLOOR_LAYOUT_FILE_NAME)
        self.world_layouts.load()
        self.world_layouts.print()

        self.load_world_properties()

    def load_world_properties(self):

        # World Properties:-
        # - world name
        # - skin name
        # - player start pos
        # - player exit pos
        # - switch -> swap tiles mapping

        switch_tiles = {(512, 288, 109): {Objects.SWITCH_TILE: (Objects.TILE2, Objects.TILE1)}}
        switch_tiles = {(512, 288, 109): {Objects.SWITCH_TILE: (Objects.EMPTY, Objects.TILE3)}}

        new_world_id = 1
        new_world_properties = ("Welcome World", "default", (224, 254, 0), (100, 562, 120), switch_tiles)
        self.world_properties[new_world_id] = new_world_properties

        new_world_id = 2
        new_world_properties = ("The Test", "test", (504, 558, 150), (104, 48, 170), switch_tiles)
        self.world_properties[new_world_id] = new_world_properties

        new_world_id = 3
        new_world_properties = ("The Next Test", "test", (504, 558, 150), (50, 100, 170), switch_tiles)
        self.world_properties[new_world_id] = new_world_properties

        for id in self.world_properties.keys():
            properties = self.world_properties[id]
            world = self.get_world(id)
            if world is not None:
                world.initialise(properties)

    def get_world(self, world_name: str):
        return self.world_layouts.get_world(world_name)


class WorldLayoutLoader():
    world_layouts = {}

    DEFAULT_OBJECT_WIDTH = 32
    DEFAULT_OBJECT_DEPTH = 32

    EMPTY_OBJECT_CODE = " "

    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):

        # Attempt to open the file
        with open(self.file_name, 'r') as object_file:

            # Load all rows in as a dictionary
            reader = csv.DictReader(object_file)

            # Get the list of column headers
            header = reader.fieldnames

            current_floor_id = None
            current_floor_layer = None

            # For each row in the file....
            for row in reader:

                world_id = int(row.get("ID"))
                world_name = row.get("Name")

                if world_id != current_floor_id:
                    WorldLayoutLoader.world_layouts[world_id] = World3D(name=world_name, w=1000, h=1000, d=1000)
                    current_floor_id = world_id
                    y = 0

                new_world = WorldLayoutLoader.world_layouts[world_id]

                floor_layer = int(row.get("Layer"))
                if floor_layer != current_floor_layer:
                    current_floor_layer = floor_layer
                    y = 0

                floor_layout = row.get("Layout")
                x = 0
                for object_code in floor_layout:
                    if object_code != WorldLayoutLoader.EMPTY_OBJECT_CODE:
                        new_floor_object = WorldObjectLoader.get_object_copy_by_code(object_code)
                        new_floor_object.set_pos((x,y,floor_layer))
                        new_world.add_object3D(new_floor_object)
                    x += WorldLayoutLoader.DEFAULT_OBJECT_WIDTH

                y += WorldLayoutLoader.DEFAULT_OBJECT_DEPTH

    def get_world(self, world_name: str):
        if world_name in self.world_layouts.keys():
            return self.world_layouts[world_name]
        else:
            print("Couldn't find world {0}".format(world_name))
            return None

    def print(self):
        print("{0} world layouts loaded".format(len(self.world_layouts.keys())))

        for key in self.world_layouts.keys():
            print("Loaded world '{0}'".format(key))


class WorldObjectLoader():
    world_objects = {}
    map_object_name_to_code = {}

    BOOL_MAP = {"TRUE": True, "FALSE": False}

    def __init__(self, file_name: str):
        self.file_name = file_name

    def load(self):

        # Attempt to open the file
        with open(self.file_name, 'r') as object_file:
            # Load all rows in as a dictionary
            reader = csv.DictReader(object_file)

            # Get the list of column headers
            header = reader.fieldnames

            # For each row in the file....
            for row in reader:
                # print("loading {0}".format(row))

                object_code = row.get("Code")

                new_object = RPGObject3D(name=row.get("Name"), \
                                         opos=(0, 0, 0), \
                                         osize=(int(row.get("width")), int(row.get("depth")), int(row.get("height"))), \
                                         solid=WorldObjectLoader.BOOL_MAP[row.get("solid").upper()], \
                                         visible=WorldObjectLoader.BOOL_MAP[row.get("visible").upper()], \
                                         interactable=WorldObjectLoader.BOOL_MAP[row.get("interactable").upper()],
                                         collectable=WorldObjectLoader.BOOL_MAP[row.get("collectable").upper()],
                                         switchable=WorldObjectLoader.BOOL_MAP[row.get("switchable").upper()]
                                         )

                # Store the floor object in the code cache
                WorldObjectLoader.world_objects[object_code] = new_object

                # Store mapping of object name to code
                WorldObjectLoader.map_object_name_to_code[new_object.name] = object_code

                logging.info("{0}.load(): Loaded Floor Object {1}".format(__class__, new_object.name))

    def print(self):
        print("{0} world objects loaded".format(len(self.world_objects.keys())))
        for obj in self.world_objects.values():
            print(str(obj))

    @staticmethod
    def get_object_copy_by_code(object_code: str):

        if object_code not in WorldObjectLoader.world_objects.keys():
            raise Exception("Can't find object by code '{0}'".format(object_code))

        return copy.deepcopy(WorldObjectLoader.world_objects[object_code])

    @staticmethod
    def get_object_copy_by_name(object_name: str):

        if object_name not in WorldObjectLoader.map_object_name_to_code.keys():
            raise Exception("Can't find object by name '{0}'".format(object_name))

        object_code = WorldObjectLoader.map_object_name_to_code[object_name]

        if object_code not in WorldObjectLoader.world_objects.keys():
            raise Exception("Can't find object by code '{0}'".format(object_name))

        return WorldObjectLoader.get_object_copy_by_code(object_code)


class World3D:
    # Define direction vectors
    INVERSE = np.array([-1, -1, -1])
    NORTH = np.array([0, 0, 1])
    SOUTH = np.multiply(NORTH, INVERSE)
    EAST = np.array([1, 0, 0])
    WEST = np.multiply(EAST, INVERSE)
    UP = np.array([0, 1, 0])
    DOWN = np.multiply(UP, INVERSE)

    HEADINGS = (NORTH, SOUTH, EAST, WEST, UP, DOWN)

    # Define states
    PLAYER_MOVING = "moving"
    PLAYER_FALLING = "falling"

    SLOW_TILES = (Objects.LIQUID1, Objects.LIQUID2)

    def __init__(self, name: str = "default", w: int = 100, h: int = 100, d: int = 100):

        self.name = name
        self.skin = "default"
        self.player_start_pos = (0, 0, 0)
        self.player_exit_pos = (0, 0, 0)
        self.width = w
        self.height = h
        self.depth = d
        self.state = World3D.PLAYER_MOVING

        self.objects = []
        self.planes = {}
        self.switches = {}
        self.switch_tiles = {}
        self.switch_groups = {}

        self.player = None

    def __str__(self):
        return "World {0}: skin({1}), size({2},{3},{4})".format(self.name, self.skin, self.width, self.height,
                                                                self.depth)

    @property
    def rect(self):
        return pygame.Rect(0, 0, self.width, self.height)

    def add_object3D(self, new_object, do_copy: bool = True):

        x, y, z = new_object.xyz

        if self.is_valid_xyz(x, y, z) is True:

            if do_copy is True:
                new_object = copy.deepcopy(new_object)

            # If this new object is a switchable object...
            if new_object.is_switchable is True:
                new_switch_object = SwitchableObject(new_object, new_object)
                if new_object.name not in self.switch_groups.keys():
                    self.switch_groups[new_object.name] = SwitchGroup(new_object.name)
                self.switch_groups[new_object.name].add_switch(new_object)

            if z not in self.planes.keys():
                self.planes[z] = []

            self.planes[z].append(new_object)

        else:
            print("Can't add object {0} at ({1},{2},{3})".format(str(new_object), x, y, z))

    def delete_object3D(self, selected_object, plane: int = None):

        x, y, z = selected_object.xyz

        if plane is not None:
            z = plane

        if z in self.planes.keys():
            selected_plane = self.planes[z]
            if selected_object in selected_plane:
                self.planes[z].remove(selected_object)
        else:
            print("Can't delete object {0} at ({1},{2},{3})".format(str(selected_object), x, y, z))

    def add_switch_group(self, new_switch_group : SwitchGroup):

        self.switch_groups[new_switch_group.name] = new_switch_group

    def get_switch_object(self, switch_tile, switch_key):

        object = switch_tile

        # If the switch_key is a valid key in this world...
        # and the switch_key has a switch_ tile map...
        # and the switch tile map has a mapping for the tile to be switched....
        if switch_key in self.switches.keys() and \
                switch_key in self.switch_tiles.keys() and \
                switch_tile.name in self.switch_tiles[switch_key].keys():

            switch_value = self.switches[switch_key]
            switch_tiles_map = self.switch_tiles[switch_key][switch_tile.name]

            if switch_value is True:
                new_object_name = switch_tiles_map[1]
            else:
                new_object_name = switch_tiles_map[0]

            if new_object_name == Objects.EMPTY:
                object = None
            else:
                object = WorldObjectLoader.get_object_copy_by_name(new_object_name)

        return object

    def add_player(self, new_player, start_pos: bool):

        self.player = new_player
        if start_pos is True:
            self.move_player_to_xyz(self.player_start_pos)
        else:
            self.move_player_to_xyz(self.player_exit_pos)

        return

    def delete_player(self):

        if self.player is not None:
            self.delete_object3D(self.player)

        return

    def is_valid_xyz(self, x, y, z):

        if x < 0 or x > int(self.width) or y < 0 or y > int(self.height) or z < 0 or z > int(self.depth):
            return False
        else:
            return True

    def is_valid_pos(self, pos):
        x, y, z = pos
        return self.is_valid_xyz(x, y, z)

    def initialise(self, world_properties=None):

        # parse the properties
        # World Properties:-
        # - world name
        # - skin name
        # - player start pos
        # - player exit pos
        # - switches to switch tiles map
        if world_properties is not None:
            self.name, self.skin, self.player_start_pos, self.player_exit_pos, self.switch_tiles = world_properties

    def move_player(self, vector):

        dx, dy, dz = vector

        if len(self.touching_objects(self.player, distance = 0, filter=World3D.SLOW_TILES)) > 0:
            print("Hitting some slowing objects")
            dx = int(dx/2)
            dy = int(dy/2)

        selected_player = self.player

        new_plane = selected_player.z + dz
        if new_plane in self.planes.keys():
            objects = self.planes[new_plane]
        else:
            objects = []

        # Are we attempting to change planes?
        if dz != 0:
            selected_player.move(0, 0, dz)

            if self.is_valid_pos(selected_player.xyz) is False:
                selected_player.back()
                print("DZ:Player {0} moving to {1} goes outside the world".format(self.player, vector))
            else:
                for object in objects:
                    if object.is_solid is True and object.is_colliding(selected_player):
                        selected_player.back()
                        # print("DZ:Player {0} collided with object {1}".format(self.player, str(object)))
                        break

        # If we succeeded in moving planes...
        if selected_player.has_changed_planes() is True:

            # print("Player has changed planes from {0} to {1}".format(self.player.z, self.player._old_z))

            # Get the objects for the new plane
            new_plane = selected_player.z
            if new_plane in self.planes.keys():
                objects = self.planes[new_plane]
            else:
                objects = []

        # Are we attempting to change X position?
        if dx != 0:
            selected_player.move(dx, 0, 0)

            if self.is_valid_pos(selected_player.get_pos()) is False:
                selected_player.back()
            else:
                for object in objects:
                    if object.is_solid is True and object.is_colliding(selected_player):
                        selected_player.back()
                        # print("DX:Player {0} collided with object {1}".format(self.player, str(object)))
                        break

        # Are we attempting to change Y position?
        if dy != 0:
            selected_player.move(0, dy, 0)

            if self.is_valid_pos(selected_player.get_pos()) is False:
                selected_player.back()
            else:
                for object in objects:
                    if object.is_solid is True and object.is_colliding(selected_player):
                        selected_player.back()
                        # print("DY:Player {0} collided with object {1}".format(self.player, str(object)))
                        break

        # did we move anywhere?
        if self.player.has_moved() is True:

            # If we succeeded in moving planes...
            if selected_player.has_changed_planes() is True:
                # Adjust the plane data to reflect new position
                self.delete_object3D(self.player, self.player._old_z)
                self.add_object3D(self.player, do_copy=False)

    def move_player_to_xyz(self, xyz):

        x, y, z = xyz

        if self.is_valid_xyz(x, y, z):
            self.delete_object3D(self.player)
            self.player.set_pos((x, y, z))
            self.add_object3D(self.player, do_copy=False)

    def move_player_to_start(self):

        self.move_player_to_xyz(self.player_start_pos)

    def move_player_to_exit(self):

        self.move_player_to_xyz(self.player_exit_pos)

    def get_player_xyz(self):
        return self.player.xyz

    def get_objects_by_plane(self, z: int = None):

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
                if self.is_collision((x, y, z), obj) is True:
                    matching_objects.append(obj)

        return matching_objects

    def touching_objects(self, target, distance = None, filter : list = None):

        objects = self.planes[target.z]

        touching = []

        for object in objects:
            if object.is_touching(target, distance):
                if filter is None:
                    touching.append(object)
                elif object.name in filter:
                    touching.append(object)

        return touching


    def swap_object(self, old_object, new_object_name):

        xyz = old_object.xyz
        new_object = WorldObjectLoader.get_object_copy_by_name(new_object_name)
        new_object.set_pos(xyz)
        self.add_object3D(new_object)
        self.delete_object3D(old_object)

    def set_switch(self, switch_key, state=None):

        if switch_key in self.switch_groups.keys():
            if state is None:
                self.switches[switch_key].switch()
            else:
                self.switches[switch_key] = state

    def print(self):

        for switch_key, setting in self.switches.items():
            print("Switch ID={0} set to {1}".format(switch_key, setting))

        for switch_key, switch_tiles in self.switch_tiles.items():
            print("Switch ID={0}: switches {1}".format(switch_key, switch_tiles))

        for switch_group in self.switch_groups.values():
            switch_group.print()