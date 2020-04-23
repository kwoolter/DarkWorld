import csv
import logging
import copy
import pygame
import numpy as np
import random
from .objects import Objects
import math

class RPGObject3D(object):
    TOUCH_FIELD_X = 4
    TOUCH_FIELD_Y = 4

    TYPE_PLAYER = "player"
    TYPE_MONSTER = "monster"

    def __init__(self, name: str,
                 type: int = 0,
                 opos=(0, 0, 0),
                 osize=(1, 1, 1),
                 solid: bool = True,
                 visible: bool = True,
                 interactable: bool = False,
                 collectable: bool = False,
                 switchable: bool = False,
                 switch=False,
                 state=False):

        self.tick_count = 0
        self.name = name
        self.type = type
        self.state = state

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
        self.is_switch = switch
        self.is_switchable = switchable
        self.is_player = False

    def __str__(self):
        return "{0} type({1}) pos({2}) id({3})".format(self.name, self.type, self.xyz, id(self))

    def tick(self):
        self.tick_count += 1

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
    def dxdydz(self):
        return (int(self._rect.x - self._old_rect.x), int(self._rect.y - self._old_rect.y), int(self._z - self._old_z))

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

    def is_touching(self, other_object, distance=None):

        if distance is None:
            touch_field = self._rect.inflate(RPGObject3D.TOUCH_FIELD_X, RPGObject3D.TOUCH_FIELD_Y)
        else:
            touch_field = self._rect.inflate(int(distance), int(distance))

        return self.z == other_object.z and \
               self.is_visible and \
               self != other_object and \
               touch_field.colliderect(other_object.rect)

    def is_inside(self, other_object):

        return self.z == other_object.z and \
               self != other_object and \
               other_object.rect.contains(self.rect)

    def contains(self, other_object):
        return self.z == other_object.z and \
               self != other_object and \
               self.rect.contains(other_object.rect)

    def contains_point(self, point):
        x, y, z = point
        # print(f'{x}:{y} collides {self.rect}={self.rect.collidepoint((x,y))}')
        return self.z == z and self.rect.collidepoint((x, y)) != 0

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


class SwitchGroup:
    # Type of switch combinations supported
    AND = "and"
    NAND = "nand"
    OR = "or"
    NOR = "nor"

    # A change to a switch changes all switches
    AND_LINKED = "and linked"

    # Cascaded XOR and XNOR implementation
    XOR = "xor"
    XNOR = "xnor"

    def __init__(self, name: str, from_object_name: str = None, to_object_name: str = None, type=AND):

        self.name = name
        self._old_output = None
        self.outputs = {False: from_object_name, True: to_object_name, None: "????"}
        self.type = type
        self.switch_objects = []

    @property
    def switches(self):
        return self.switch_objects

    @switches.setter
    def switches(self, new_switches):
        self.switch_objects = new_switches

    def set_from_to(self, from_object_name: str, to_object_name: str):
        self.outputs[False] = from_object_name
        self.outputs[True] = to_object_name

    def has_changed_state(self):
        new_state = self.output()
        return self._old_output != new_state

    def add_switch(self, new_switch, value: bool = False):

        if new_switch not in self.switch_objects:
            self.switch_objects.append(new_switch)

        if value not in (True, False):
            value = False

        new_switch.state = value

    def remove_switch(self, old_switch):

        if old_switch in self.switch_objects:
            self.switch_objects.remove(old_switch)

    def switch(self, switch_object, value=None):

        self._old_output = self.output()

        if switch_object not in self.switch_objects:
            # print("trying to switch an object not in this group {0}".format(self.name))
            self.add_switch(switch_object, switch_object.state)

        if value is None:
            value = not switch_object.state

        switch_object.state = value

        if self.type == SwitchGroup.AND_LINKED:
            for switch_object in self.switch_objects:
                switch_object.state = value

        return self.output()

    def output(self):

        result = False
        or_result = False
        and_result = True
        xor_result = False

        for switch in self.switch_objects:
            switch_state = switch.state
            or_result = or_result or switch_state
            and_result = and_result and switch_state
            xor_result = abs(xor_result - switch_state) > 0

        if self.type in (SwitchGroup.AND, SwitchGroup.AND_LINKED):
            result = and_result

        elif self.type == SwitchGroup.NAND:
            result = not and_result

        elif self.type == SwitchGroup.OR:
            result = or_result

        elif self.type == SwitchGroup.NOR:
            result = not or_result

        elif self.type == SwitchGroup.XOR:
            result = xor_result

        elif self.type == SwitchGroup.XNOR:
            result = not xor_result

        return result

    def print(self):
        print("Switch group name='{0}': type=({1}), switches={2}, output={3}".format(self.name,
                                                                                     self.type,
                                                                                     len(self.switches),
                                                                                     self.output()))

        for obj in self.switch_objects:
            print("\tswitch:{0}={1}".format(str(obj), obj.state))


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
        self.load_moving_objects()
        self.load_npcs()

    def load_npcs(self):

        world = self.get_world(1)
        world.add_npc(name="The Master", object_id=Objects.NPC1, xyz=(4 * 32, 9 * 32, 20), vanish=True,
                      gift_id=Objects.BOSS_KEY)

        world = self.get_world(5)
        world.add_npc(name="The Imprisoned One", object_id=Objects.NPC2, xyz=(2 * 32, 13 * 32, 50), vanish=True)

        world = self.get_world(7)
        world.add_npc(name="The Master", object_id=Objects.NPC1, xyz=(18 * 32, 6 * 32, 20), vanish=True,
                      gift_id=Objects.BOSS_KEY)

        world = self.get_world(9)
        world.add_npc(name="Rosie", object_id=Objects.NPC1, xyz=(1 * 32, 1 * 32, 50), vanish=True,
                      gift_id=Objects.BOSS_KEY)
        world.add_npc(name="Skids", object_id=Objects.NPC2, xyz=(18 * 32, 1 * 32, 50))

        world = self.get_world(100)
        world.add_npc(name="The Jailer", object_id=Objects.NPC1, xyz=(5 * 32, 12 * 32, 30))

    def load_moving_objects(self):

        # World 1
        world = self.get_world(1)
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY1)
        new_monster.set_pos((4 * 32, 13 * 32, 20))
        ai = AIBotRandom(new_monster, world)
        ai.set_instructions((World3D.UP, World3D.DOWN, World3D.DUMMY, World3D.WEST, World3D.EAST),
                            min_duration=10,
                            max_duration=20)

        world.add_monster(new_monster, World3D.DUMMY, ai)



        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY2)
        new_monster.set_pos((4 * 32, 6 * 32, 20))
        ai = AIBotHunter(new_monster, world, tick_slow_factor=1)
        ai.set_instructions(new_target=None, route = [(4 * 32, 6 * 32, 20), (4 * 32, 14 * 32, 20), (7 * 32, 10 * 32, 20), (10 * 32, 10 * 32, 20)])
        world.add_monster(new_monster, World3D.DUMMY, ai)

        # World 2
        world = self.get_world(2)
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY1)
        new_monster.set_pos((6 * 32, 10 * 32, 20))
        ai = AIBotRouteFollowing(new_monster, world, tick_slow_factor=1)
        ai.set_instructions([(4 * 32, 6 * 32, 20), (4 * 32, 14 * 32, 20), (7 * 32, 10 * 32, 20), (10 * 32, 10 * 32, 20)])

        world.add_monster(new_monster, World3D.DUMMY, ai)

        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY2)
        new_monster.set_pos((4 * 32, 6 * 32, 20))
        ai = AIBotRouteFollowing(new_monster, world, tick_slow_factor=2)
        ai.set_instructions([(4 * 32, 6 * 32, 20), (4 * 32, 14 * 32, 20), (7 * 32, 10 * 32, 20), (10 * 32, 10 * 32, 20)])
        world.add_monster(new_monster, World3D.DUMMY, ai)

        # World 3
        world = self.get_world(3)
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY1)
        new_monster.set_pos((15 * 32, 6 * 32, 20))

        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.UP, 32 * 8, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DOWN, 32 * 8, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                        ]
        ai.set_instructions(instructions)

        world.add_monster(new_monster, World3D.DUMMY, ai)

        # World 4
        world = self.get_world(4)
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY1)
        new_monster.set_pos((15 * 32, 6 * 32, 20))

        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.UP * 2, 32 * 8, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DOWN * 2, 32 * 8, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                        ]
        ai.set_instructions(instructions)

        world.add_monster(new_monster, World3D.DUMMY, ai)

        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY1)
        new_monster.set_pos((11 * 32, 13 * 32, 20))

        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.UP * 2, 32 * 8, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DOWN * 2, 32 * 8, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                        ]
        ai.set_instructions(instructions)

        world.add_monster(new_monster, World3D.DUMMY, ai)

        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY2)
        new_monster.set_pos((11 * 32, int(9.5 * 32), 20))

        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.WEST * 2, 32 * 10, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.EAST * 2, 32 * 10, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                        ]
        ai.set_instructions(instructions)

        world.add_monster(new_monster, World3D.DUMMY, ai)

        # World 5
        world = self.get_world(5)

        for i in range(0, 2):
            new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.MONSTER2)
            new_monster.set_pos((12 * 32, (9 + i) * 32, 51))

            ai = AIBotInstructions(new_monster, world)
            instructions = [(World3D.EAST, 128, AIBot.INSTRUCTION_FAIL_SKIP),
                            (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                            (World3D.WEST, 128, AIBot.INSTRUCTION_FAIL_SKIP),
                            (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                            ]
            ai.set_instructions(instructions)

            world.add_monster(new_monster, World3D.DUMMY, ai)

        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY2)
        new_monster.set_pos((11 * 32, 7 * 32, 50))

        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.UP, 32 * 6, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DOWN, 32 * 6, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                        ]
        ai.set_instructions(instructions)

        world.add_monster(new_monster, World3D.DUMMY, ai)

        # World 8
        world = self.get_world(8)

        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY2)
        new_monster.set_pos((3 * 32, 17 * 32, 50))

        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.EAST, 32 * 15, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.WEST, 32 * 15, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                        ]
        ai.set_instructions(instructions)

        world.add_monster(new_monster, World3D.DUMMY, ai)

        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY2)
        new_monster.set_pos((3 * 32, 2 * 32, 50))

        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.EAST, 32 * 15, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.WEST, 32 * 15, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                        ]
        ai.set_instructions(instructions)

        world.add_monster(new_monster, World3D.DUMMY, ai)

        for i in range(0, 2):
            new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.MONSTER2)
            new_monster.set_pos((3 * 32, (9 + i) * 32, 21))

            ai = AIBotInstructions(new_monster, world)
            instructions = [(World3D.EAST, 32 * 15, AIBot.INSTRUCTION_FAIL_SKIP),
                            (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                            (World3D.WEST, 32 * 15, AIBot.INSTRUCTION_FAIL_SKIP),
                            (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                            ]
            ai.set_instructions(instructions)

            world.add_monster(new_monster, World3D.DUMMY, ai)

            new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.MONSTER1)
            new_monster.set_pos((17 * 32, (9 + i) * 32, 120))

            ai = AIBotInstructions(new_monster, world)
            instructions = [(World3D.EAST, 32 * 15, AIBot.INSTRUCTION_FAIL_SKIP),
                            (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                            (World3D.WEST, 32 * 15, AIBot.INSTRUCTION_FAIL_SKIP),
                            (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                            ]
            ai.set_instructions(instructions)

            world.add_monster(new_monster, World3D.DUMMY, ai)

        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.MONSTER2)
        new_monster.set_pos((17 * 32, 8 * 32, 21))

        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.DOWN, 32 * 5, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.UP, 32 * 5, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                        ]
        ai.set_instructions(instructions)

        world.add_monster(new_monster, World3D.DUMMY, ai)

        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.MONSTER2)
        new_monster.set_pos((17 * 32, (11) * 32, 21))

        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.DOWN, 32 * 5, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.UP, 32 * 5, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                        ]
        ai.set_instructions(instructions)

        world.add_monster(new_monster, World3D.DUMMY, ai)

        # World 9
        world = self.get_world(9)
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY1)
        new_monster.set_pos((5 * 32, 11 * 32, 50))

        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.EAST * 2, 32 * 10, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DUMMY, 50, False),
                        (World3D.WEST * 2, 32 * 10, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DUMMY, 50, False)
                        ]
        ai.set_instructions(instructions)

        world.add_monster(new_monster, World3D.DUMMY, ai)

        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY2)
        new_monster.set_pos((15 * 32, 16 * 32, 50))

        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.WEST, 32 * 10, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.EAST, 32 * 10, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                        ]
        ai.set_instructions(instructions)

        world.add_monster(new_monster, World3D.DUMMY, ai)

        # World 10
        world = self.get_world(10)

        # Enemy 1
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY1)
        new_monster.set_pos((32 * 9, 32 * 10, 79))

        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.DOWN, 32 * 6, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 30, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.UP, 32 * 6, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 30, AIBot.INSTRUCTION_FAIL_TICK)
                        ]
        ai.set_instructions(instructions)

        world.add_monster(new_monster, World3D.DUMMY, ai)

        # Enemy 2
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY2)
        new_monster.set_pos((32 * 6, 32 * 12, 79))
        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.EAST, 32 * 10, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.WEST, 32 * 10, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)
                        ]
        ai.set_instructions(instructions)
        world.add_monster(new_monster, World3D.DUMMY, ai)

        # World 20
        world = self.get_world(20)

        # Monster 1 - moving block
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.MONSTER1)
        new_monster.set_pos((10 * 32, 14 * 32, 66))
        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.DOWN, 1000, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.UP, 1000, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)]
        ai.set_instructions(instructions)
        world.add_monster(new_monster, World3D.DUMMY, ai)

        # Monster #2 - moving block
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.MONSTER2)
        new_monster.set_pos((200, 544, 66))
        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.EAST, 1000, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.WEST, 1000, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DOWN, 32 * 5, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.UP, 32 * 5, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        ]
        ai.set_instructions(instructions)
        world.add_monster(new_monster, World3D.DUMMY, ai)

        # Monster #3 - Lift
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.BIG_MONSTER2)
        new_monster.set_pos((48, 196, 70))
        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.NORTH, 1000, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.SOUTH, 1000, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 10, AIBot.INSTRUCTION_FAIL_TICK)]
        ai.set_instructions(instructions)
        world.add_monster(new_monster, World3D.DUMMY, ai)

        # Enemy #1
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY1)
        new_monster.set_pos((32 * 2, 32 * 8, 60))
        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.UP, 9 * 32, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DOWN, 9 * 32, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)]
        ai.set_instructions(instructions)
        world.add_monster(new_monster, World3D.DUMMY, ai)

        # World 100
        world = self.get_world(100)

        # Monster #1
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY1)
        new_monster.set_pos((32 * 12, 32 * 7, 60))
        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.UP, 6 * 32, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.DOWN, 6 * 32, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)]
        ai.set_instructions(instructions)
        world.add_monster(new_monster, World3D.DUMMY, ai)

        # Monster #2
        new_monster = WorldObjectLoader.get_object_copy_by_name(Objects.ENEMY2)
        new_monster.set_pos((32 * 4, 32 * 9, 60))
        ai = AIBotInstructions(new_monster, world)
        instructions = [(World3D.EAST, 10 * 32, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK),
                        (World3D.WEST, 10 * 32, AIBot.INSTRUCTION_FAIL_SKIP),
                        (World3D.DUMMY, 50, AIBot.INSTRUCTION_FAIL_TICK)]
        ai.set_instructions(instructions)
        world.add_monster(new_monster, World3D.DUMMY, ai)

    def load_world_properties(self):

        # World Properties:-
        # - world name
        # - skin name
        # - player start pos
        # - player exit pos
        # - switch group settings

        # World 1
        switch_groups = {
            Objects.SWITCH_1: (Objects.SWITCH_TILE1, Objects.TILE1, SwitchGroup.OR)}

        new_world_id = 1
        new_world_properties = ("Dark World", "tutorial", (66, 300, 0), (528, 240, 0), switch_groups)
        self.world_properties[new_world_id] = new_world_properties

        # World 2
        switch_groups = {
            Objects.SWITCH_1: (Objects.SWITCH_TILE1, Objects.TILE1, SwitchGroup.AND_LINKED)}

        new_world_id += 1
        new_world_properties = ("Tutorial World 2", "tutorial", (66, 300, 0), (528, 240, 0), switch_groups)
        self.world_properties[new_world_id] = new_world_properties

        # World 3
        switch_groups = {
            Objects.SWITCH_1: (Objects.SWITCH_TILE1, Objects.TILE1, SwitchGroup.OR)}

        new_world_id += 1
        new_world_properties = ("Tutorial World 3", "tutorial", (66, 300, 0), (528, 240, 0), switch_groups)
        self.world_properties[new_world_id] = new_world_properties

        # World 4
        switch_groups = {
            Objects.SWITCH_1: (Objects.SWITCH_TILE1, Objects.TILE1, SwitchGroup.AND)}

        new_world_id += 1
        new_world_properties = ("Tutorial World 4", "tutorial", (66, 300, 0), (528, 240, 0), switch_groups)
        self.world_properties[new_world_id] = new_world_properties

        # World 5
        new_world_id += 1
        new_world_properties = ("Tutorial World 5", "tutorial2", (80, 306, 0), (474, 300, 40), None)
        self.world_properties[new_world_id] = new_world_properties

        # World 6
        new_world_id += 1
        new_world_properties = ("Tutorial World 6", "tutorial2", (66, 300, 0), (528, 358, 20), None)
        self.world_properties[new_world_id] = new_world_properties

        # World 7
        switch_groups = {
            Objects.SWITCH_1: (Objects.SWITCH_TILE1, Objects.KEY, SwitchGroup.AND)}

        new_world_id += 1
        new_world_properties = (
        "Tutorial World {0}".format(new_world_id), "tutorial2", (66, 300, 0), (528, 358, 20), switch_groups)
        self.world_properties[new_world_id] = new_world_properties

        # World 8
        switch_groups = {
            Objects.SWITCH_1: (Objects.SWITCH_TILE1, Objects.TILE1, SwitchGroup.NAND),
            Objects.SWITCH_2: (Objects.SWITCH_TILE2, Objects.WALL1, SwitchGroup.NAND),
            Objects.SWITCH_3: (Objects.SWITCH_TILE3, Objects.TILE3, SwitchGroup.OR),
            Objects.SWITCH_4: (Objects.SWITCH_TILE4, Objects.TILE4, SwitchGroup.NAND)}

        new_world_id += 1
        new_world_properties = (
        "Tutorial World {0}".format(new_world_id), "tutorial2", (50, 104, 0), (528, 358, 0), switch_groups)
        self.world_properties[new_world_id] = new_world_properties

        # World 9
        new_world_id += 1
        new_world_properties = (
        "Tutorial World {0}".format(new_world_id), "tutorial2", (66, 300, 0), (528, 240, 0), None)
        self.world_properties[new_world_id] = new_world_properties

        # World 10
        switch_groups = {
            Objects.SWITCH_1: (Objects.SWITCH_TILE1, Objects.TILE1, SwitchGroup.OR),
            Objects.SWITCH_2: (Objects.SWITCH_TILE2, Objects.TILE2, SwitchGroup.AND),
            Objects.SWITCH_4: (Objects.SWITCH_TILE4, Objects.TILE4, SwitchGroup.AND)
        }

        new_world_id = 10
        new_world_properties = ("Insanity", "world10", (224, 254, 0), (102, 244, 0), switch_groups)
        self.world_properties[new_world_id] = new_world_properties

        # World 20
        switch_groups = {
            Objects.SWITCH_1: (Objects.SWITCH_TILE1, Objects.TILE1, SwitchGroup.OR),
            Objects.SWITCH_2: (Objects.SWITCH_TILE2, Objects.TILE2, SwitchGroup.XNOR),
            Objects.SWITCH_3: (Objects.SWITCH_TILE3, Objects.BOSS_KEY, SwitchGroup.AND),
            Objects.SWITCH_4: (Objects.SWITCH_TILE4, Objects.TILE3, SwitchGroup.OR)
        }

        new_world_id = 20
        new_world_properties = ("The Challenge", "world10", (560, 112, 0), (104, 48, 0), switch_groups)
        self.world_properties[new_world_id] = new_world_properties

        # World 30
        new_world_id = 30
        new_world_properties = ("The Next Test", "world10", (504, 558, 150), (50, 100, 170), switch_groups)
        self.world_properties[new_world_id] = new_world_properties

        # World 100
        switch_groups = {
            Objects.SWITCH_1: (Objects.SWITCH_TILE1, Objects.TILE1, SwitchGroup.OR),
            Objects.SWITCH_2: (Objects.SWITCH_TILE2, Objects.TILE2, SwitchGroup.OR),
            Objects.SWITCH_3: (Objects.SWITCH_TILE3, Objects.TILE3, SwitchGroup.XOR),
            Objects.SWITCH_4: (Objects.SWITCH_TILE4, Objects.WALL1, SwitchGroup.NAND)}

        new_world_id = 100
        new_world_properties = ("Dungeon World", "dungeon", (46, 302, 0), (32 * 5.5, 32 * 3.5, 0), switch_groups)
        self.world_properties[new_world_id] = new_world_properties

        # Load up all of the properties that we have defined
        for id in self.world_properties.keys():
            properties = self.world_properties[id]
            world = self.get_world(id)
            if world is not None:
                world.initialise(properties)

    def get_world(self, world_name: str, do_copy: bool = False):

        if do_copy is True:
            return copy.deepcopy(self.world_layouts.get_world(world_name))
        else:
            return self.world_layouts.get_world(world_name)

    def get_world_names(self):
        return self.world_layouts.get_world_names()


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
                        new_floor_object.set_pos((x, y, floor_layer))
                        new_world.add_object3D(new_floor_object, do_copy=False)
                    x += WorldLayoutLoader.DEFAULT_OBJECT_WIDTH

                y += WorldLayoutLoader.DEFAULT_OBJECT_DEPTH

    def get_world(self, world_name: str):
        if world_name in self.world_layouts.keys():
            return self.world_layouts[world_name]
        else:
            print("Couldn't find world {0}".format(world_name))
            return None

    def get_world_names(self):
        return sorted(list(self.world_layouts.keys()))

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
                                         switchable=WorldObjectLoader.BOOL_MAP[row.get("switchable").upper()],
                                         switch=WorldObjectLoader.BOOL_MAP[row.get("switch").upper()]
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
    DUMMY = np.array([0, 0, 0])
    INVERSE = np.array([-1, -1, -1])
    NORTH = np.array([0, 0, 1])
    SOUTH = np.multiply(NORTH, INVERSE)
    EAST = np.array([1, 0, 0])
    WEST = np.multiply(EAST, INVERSE)
    UP = np.array([0, 1, 0])
    DOWN = np.multiply(UP, INVERSE)

    HEADINGS = (NORTH, SOUTH, EAST, WEST, UP, DOWN)

    # Define states
    STATE_LOADED = "loaded"
    STATE_READY = "ready"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_GAME_OVER = "game over"

    PLAYER_MOVING = "moving"
    PLAYER_FALLING = "falling"

    SLOW_TILES = (Objects.LIQUID1, Objects.LIQUID2)
    ENEMIES = (Objects.ENEMY1, Objects.ENEMY2)

    def __init__(self, name: str = "default", w: int = 100, h: int = 100, d: int = 100):

        # World propoerties
        self.name = name
        self.skin = "default"
        self.player_start_pos = (0, 0, 0)
        self.player_exit_pos = (0, 0, 0)
        self.width = w
        self.height = h
        self.depth = d
        self.state = World3D.STATE_LOADED
        self.player_state = World3D.PLAYER_MOVING
        self.tick_count = 0

        # World contents
        self.planes = {}
        self.monsters = {}
        self.bots = []
        self._npcs = {}
        self.switch_groups = {}

        self.player = None

    def __str__(self):
        return "World {0}: skin({1}), size({2},{3},{4})".format(self.name, self.skin, self.width, self.height,
                                                                self.depth)

    @property
    def max_plane_depth(self):
        return max(self.planes.keys())

    @property
    def rect(self):
        return pygame.Rect(0, 0, self.width, self.height)

    def add_object3D(self, new_object, do_copy: bool = True):

        x, y, z = new_object.xyz

        if self.is_valid_xyz(x, y, z) is True:

            if do_copy is True:
                new_object = copy.deepcopy(new_object)

            # If this new object is a switch object...
            if new_object.is_switch is True:
                self.add_switch_object(new_object)

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
                # del selected_object
        else:
            print("Can't delete object {0} at ({1},{2},{3})".format(str(selected_object), x, y, z))

    def add_switch_group(self, new_switch_group: SwitchGroup):

        if new_switch_group.name in self.switch_groups.keys():
            print("Already got a switch group with id {0}".format(new_switch_group.name))
            for switch in self.switch_groups[new_switch_group.name].switches:
                new_switch_group.add_switch(switch)

        self.switch_groups[new_switch_group.name] = new_switch_group

    def add_switch_object(self, new_object):

        if new_object.name not in self.switch_groups.keys():
            self.add_switch_group(SwitchGroup(name=new_object.name, from_object_name=new_object.name))

        print("adding a switch object".format(str(new_object)))

        self.switch_groups[new_object.name].add_switch(new_object)

    def add_player(self, new_player, start_pos: bool):

        self.player = new_player
        if start_pos is True:
            self.move_player_to_xyz(self.player_start_pos)
        else:
            self.move_player_to_xyz(self.player_exit_pos)

        for ai in self.bots:
            if isinstance(ai, (AIBotTracker, AIBotHunter)) is True:
                ai.set_instructions(self.player)

        return

    def add_npc(self, name: str, object_id: str, xyz: tuple, vanish=False, gift_id=None):
        new_npc = WorldObjectLoader.get_object_copy_by_name(object_id)
        new_npc.set_pos(xyz)
        self.add_object3D(new_npc, do_copy=False)
        self._npcs[object_id] = name, vanish, gift_id

    def get_npc_details(self, object_id: str):
        if object_id in self._npcs.keys():
            return self._npcs[object_id]
        else:
            return None

    # def talk_to_npc(self, npc_id):
    #     npc_name, vanish, gift_id = self.get_npc_details(npc_id)
    #     if npc_name is not None:
    #         print("talk to {0}".format(npc_name))

    def add_monster(self, new_monster, move_vector, ai=None):
        self.monsters[new_monster] = move_vector
        if ai is not None:
            self.bots.append(ai)
            if isinstance(ai, AIBotTracker) is True:
                ai.set_instructions(self.player)
        self.add_object3D(new_monster, do_copy=False)

    def move_monsters(self, override_vector=None, reverse=True):

        for bot in self.bots:
            bot.tick()

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

    def is_player_dead(self):

        dead = False

        if self.player.z >= (self.depth - 50):
            dead = True
            print("dead")

        return dead

    def initialise(self, world_properties=None):

        # parse the properties
        # World Properties:-
        # - world name
        # - skin name
        # - player start pos
        # - player exit pos
        # - switch groups settings - ID, from, to, type

        if world_properties is not None:
            self.name, self.skin, self.player_start_pos, self.player_exit_pos, switch_group_settings = world_properties

            if switch_group_settings is not None:
                for switch_id, settings in switch_group_settings.items():
                    from_object, to_object, type = settings
                    self.add_switch_group(SwitchGroup(name=switch_id,
                                                      from_object_name=from_object,
                                                      to_object_name=to_object,
                                                      type=type))

        #  Set the switch tiles based on the initial output of the switches
        for switch_group in self.switch_groups.values():
            output = switch_group.output()
            self.swap_objects_by_name(target_object_name=switch_group.outputs[not output],
                                      new_object_name=switch_group.outputs[output])

        # Set the end of the world to be the biggest plane depth + 100
        self.depth = max(self.planes.keys()) + 100

        self.state = World3D.STATE_READY

        self.print()

    def pause(self, pause_on=None):

        if pause_on is True:
            self.state = World3D.STATE_PAUSED
        elif pause_on is False and self.state == World3D.STATE_PAUSED:
            self.state = World3D.STATE_PLAYING
        elif pause_on is None:
            if self.state == World3D.STATE_PAUSED:
                self.state = World3D.STATE_PLAYING
            elif self.state == World3D.STATE_PLAYING:
                self.state = World3D.STATE_PAUSED
        print("World state={0}".format(self.state))

    def tick(self):

        self.tick_count += 1
        self.move_monsters()

    def move_player(self, vector):
        self.move_object(self.player, vector)

    def move_object(self, selected_object, vector):

        dx, dy, dz = vector

        if len(self.touching_objects(selected_object, distance=0, filter=World3D.SLOW_TILES)) > 0:
            # print("Hitting some slowing objects")
            dx = int(dx / 2)
            dy = int(dy / 2)

        new_plane = selected_object.z + dz
        if new_plane in self.planes.keys():
            objects = self.planes[new_plane]
        else:
            objects = []

        # Are we attempting to change planes?
        if dz != 0:
            selected_object.move(0, 0, dz)

            if self.is_valid_pos(selected_object.xyz) is False:
                selected_object.back()
                # print("DZ:Object {0} moving to {1} goes outside the world".format(selected_object, vector))
            else:
                for object in objects:
                    if object.is_solid is True and object.is_colliding(selected_object):
                        selected_object.back()
                        # print("DZ:Object {0} collided with object {1}".format(selected_object, str(object)))
                        break

        # If we succeeded in moving planes...
        if selected_object.has_changed_planes() is True:

            # Get the objects for the new plane
            new_plane = selected_object.z
            if new_plane in self.planes.keys():
                objects = self.planes[new_plane]
            else:
                objects = []

        # Are we attempting to change X position?
        if dx != 0:
            selected_object.move(dx, 0, 0)

            if self.is_valid_pos(selected_object.get_pos()) is False:
                selected_object.back()
            else:
                for object in objects:
                    if object.is_solid is True and object.is_colliding(selected_object):
                        selected_object.back()
                        # print("DX:Object {0} collided with object {1}".format(selected_object, str(object)))
                        break

        # Are we attempting to change Y position?
        if dy != 0:
            selected_object.move(0, dy, 0)

            if self.is_valid_pos(selected_object.get_pos()) is False:
                selected_object.back()
            else:
                for object in objects:
                    if object.is_solid is True and object.is_colliding(selected_object):
                        selected_object.back()
                        # print("DY:Object {0} collided with object {1}".format(selected_object, str(object)))
                        break

        # did we move anywhere?
        if selected_object.has_moved() is True:

            # If we succeeded in moving planes...
            if selected_object.has_changed_planes() is True:
                # Adjust the plane data to reflect new position
                self.delete_object3D(selected_object, selected_object._old_z)
                self.add_object3D(selected_object, do_copy=False)
            # Otherwise tick the object to trigger animation.
            else:
                selected_object.tick()

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

    def touching_objects(self, target, distance=None, filter: list = None):

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
        new_object.is_switchable = True
        new_object.set_pos(xyz)
        self.add_object3D(new_object)
        self.delete_object3D(old_object)

    def swap_objects_by_name(self, target_object_name: str, new_object_name: str):

        # Collect the list of objects that need to be swapped
        objects_to_swap = []
        for plane in self.planes.values():
            for obj in plane:
                if obj.name == target_object_name and obj.is_switchable is True:
                    objects_to_swap.append(obj)

        # Swap each object that we found matching
        for obj in objects_to_swap:
            self.swap_object(obj, new_object_name)

        print("{0} world objects swapped from {1} to {2}".format(len(objects_to_swap), target_object_name,
                                                                 new_object_name))

    def set_switch(self, switch_key, state=None):

        output = None

        if switch_key in self.switch_groups.keys():
            if state is None:
                output = self.switches[switch_key].switch()
            else:
                output = self.switches[switch_key] = state

        return output

    def set_switch_object(self, object, new_state=None):

        # bject.tick()

        # if object.state not in (True, False):
        #     object.state = False
        #
        # if state is None:
        #     object.state = not object.state
        # else:
        #     object.state = state

        if object.name in self.switch_groups.keys():
            switch_group = self.switch_groups[object.name]
            output = switch_group.switch(object, new_state)
            if switch_group.has_changed_state() is True:
                print("swapping")
                self.swap_objects_by_name(target_object_name=switch_group.outputs[not output],
                                          new_object_name=switch_group.outputs[output])
        else:
            print("I don't have a switch group called {0} in this world".format(object.name))

    def print(self):

        for monster, vector in self.monsters.items():
            print("Monster {0} moving {1}".format(monster, vector))

        for switch_group in self.switch_groups.values():
            switch_group.print()

        for bot in self.bots:
            print(str(bot))

        for plane_objects in self.planes.values():
            for obj in plane_objects:
                if obj.is_switch is True:
                    print("Swicth: {0}".format(str(obj)))


class AIBot:

    INSTRUCTION_FAIL_NOP = "NOP"
    INSTRUCTION_FAIL_TICK = "TICK"
    INSTRUCTION_FAIL_SKIP = "SKIP"
    INSTRUCTION_FAIL_VALID_OPTIONS = (INSTRUCTION_FAIL_NOP, INSTRUCTION_FAIL_SKIP, INSTRUCTION_FAIL_TICK)

    def __init__(self, name: str, target_object: RPGObject3D, world: World3D, tick_slow_factor : int = 1):
        self.name = name
        self.target_object = target_object
        self.world = world
        self.tick_slow_factor = tick_slow_factor
        self.loop = False
        self.tick_count = 1

    def tick(self):
        self.tick_count += 1
        return self.tick_count % self.tick_slow_factor == 0


class AIBotInstructions(AIBot):

    def __init__(self, target_object: RPGObject3D, world: World3D, tick_slow_factor : int = 1):

        super(AIBotInstructions, self).__init__(str(__class__), target_object, world, tick_slow_factor)

        self.instructions = []
        self.current_instruction_id = 0
        self.current_instruction_ticks = 0

    def __str__(self):

        text = "{0} Bot: loop({1}), instructions:".format(self.name, self.loop)
        for instruction in self.instructions:
            action, ticks, skip_on_fail = instruction
            text += "\n\t action({0}), ticks {1}), skip on fail({2})".format(action, ticks, skip_on_fail)

        return text

    def set_instructions(self, new_instructions: list, loop: bool = True):

        self.instructions = new_instructions
        self.loop = loop

    def tick(self):

        if super(AIBotInstructions, self).tick() is False:
            return

        if self.current_instruction_id < len(self.instructions) and self.current_instruction_id >= 0:

            current_instruction = self.instructions[self.current_instruction_id]
            action, ticks, action_on_fail = current_instruction

            # If the next instruction requires an action...
            if action is not None:

                if action_on_fail not in AIBot.INSTRUCTION_FAIL_VALID_OPTIONS:
                    action_on_fail = AIBot.INSTRUCTION_FAIL_TICK

                self.world.move_object(self.target_object, action)
                success = self.target_object.has_moved()

            # If no action then success is always true
            else:
                success = True

            # If instruction succeeded...
            if success is True:
                self.current_instruction_ticks += 1
                if self.current_instruction_ticks > ticks:
                    self.next_instruction()

            # If the instruction failed then determine what to do next based on option
            else:
                if action_on_fail == AIBot.INSTRUCTION_FAIL_NOP:
                    pass
                elif action_on_fail == AIBot.INSTRUCTION_FAIL_TICK:
                    self.current_instruction_ticks += 1
                    if self.current_instruction_ticks > ticks:
                        self.next_instruction()
                elif action_on_fail == AIBot.INSTRUCTION_FAIL_SKIP:
                    self.next_instruction()

        else:
            pass
            # print("current instruction id {0} not in range".format(self.current_instruction_id))

    def next_instruction(self):

        self.current_instruction_id += 1

        if self.current_instruction_id >= len(self.instructions) and self.loop is True:
            self.current_instruction_id = 0

        self.current_instruction_ticks = 0


class AIBotRouteFollowing(AIBot):

    def __init__(self, target_object: RPGObject3D, world: World3D, tick_slow_factor : int = 1):

        super(AIBotRouteFollowing, self).__init__(str(__class__), target_object, world, tick_slow_factor)

        self.way_points = []
        self.current_instruction_id = 0
        self.failed_ticks = 0
        self.failed_ticks_limit = 10


    def __str__(self):

        text = "{0} Bot: way points:{1} current target:{2} current position:{3}".format(self.name,
                                                                                        str(self.way_points),
                                                                                        str(self.way_points[
                                                                                                self.current_instruction_id]),
                                                                                        str(self.target_object.xyz))

        return text

    def set_instructions(self, new_instructions: list, loop: bool = True):

        if new_instructions is None:
            return

        self.way_points = new_instructions
        self.loop = loop

    def tick(self):

        if super(AIBotRouteFollowing, self).tick() is False:
            return

        current_way_point = self.way_points[self.current_instruction_id]
        cx, cy, cz = current_way_point
        x = self.target_object.rect.centerx
        y = self.target_object.rect.centery
        z = self.target_object.z

        if self.target_object.contains_point(current_way_point) is True:
            self.next_instruction()

        if cz == z:
            if cx != x:
                if cx < x:
                    action = World3D.WEST
                elif cx > x:
                    action = World3D.EAST
                self.world.move_object(self.target_object, action)
                m1 = self.target_object.has_moved()
            else:
                m1 = False

            if cy != y:
                if cy < y:
                    action = World3D.DOWN
                elif cy > y:
                    action = World3D.UP
                self.world.move_object(self.target_object, action)
                m2 = self.target_object.has_moved()
            else:
                m2 = False

            if (m1 or m2) is True:
                self.failed_ticks = 0
            else:
                self.failed_ticks +=1
                if self.failed_ticks > self.failed_ticks_limit:
                    self.next_instruction()


    def next_instruction(self):

        self.current_instruction_id += 1

        if self.current_instruction_id >= len(self.way_points):
            self.current_instruction_id = 0

        self.failed_ticks = 0



class AIBotTracker(AIBot):

    def __init__(self, target_object: RPGObject3D, world: World3D, tick_slow_factor : int = 1):

        super(AIBotTracker, self).__init__(str(__class__), target_object, world, tick_slow_factor)

        self.following_object = None
        self.failed_ticks = 0
        self.failed_ticks_limit = 10

    def __str__(self):

        text = "{0} Bot: current target:{2} current position:{3}".format(self.name,
                                                                         str(self.following_object),
                                                                         str(self.target_object.xyz))

        return text

    def set_instructions(self, new_target: RPGObject3D, loop: bool = True):

        self.following_object = new_target
        self.loop = loop

    def tick(self):

        if super(AIBotTracker, self).tick() is False or self.following_object is None:
            return

        cx = self.following_object.rect.centerx
        cy = self.following_object.rect.centery
        cz = self.following_object.z

        x = self.target_object.rect.centerx
        y = self.target_object.rect.centery
        z = self.target_object.z

        if cz == z:
            if cx != x:
                if cx < x:
                    action = World3D.WEST
                elif cx > x:
                    action = World3D.EAST
                self.world.move_object(self.target_object, action)
                m1 = self.target_object.has_moved()
            else:
                m1 = False

            if cy != y:
                if cy < y:
                    action = World3D.DOWN
                elif cy > y:
                    action = World3D.UP
                self.world.move_object(self.target_object, action)
                m2 = self.target_object.has_moved()
            else:
                m2 = False

            if (m1 or m2) is True:
                self.failed_ticks = 0
            else:
                self.failed_ticks +=1



class AIBotHunter(AIBot):

    def __init__(self, target_object: RPGObject3D, world: World3D, tick_slow_factor : int = 1):

        super(AIBotHunter, self).__init__(str(__class__), target_object, world, tick_slow_factor)

        self.following_object = None
        self.visibility_distance = None
        self.failed_ticks = 0
        self.failed_ticks_limit = 10

        self.tracker = AIBotTracker(target_object=target_object, world=world, tick_slow_factor= tick_slow_factor)
        self.router = AIBotRouteFollowing(target_object=target_object, world=world, tick_slow_factor= tick_slow_factor)


    def __str__(self):

        text = "{0} Bot: current target:{2} current position:{3}".format(self.name,
                                                                         str(self.following_object),
                                                                         str(self.target_object.xyz))

        return text

    def set_instructions(self, new_target: RPGObject3D = None, distance : float = 150, route : list = None, loop: bool = True):

        self.visibility_distance = distance
        self.following_object = new_target
        self.tracker.set_instructions(new_target)
        self.router.set_instructions(new_instructions=route, loop=loop)
        self.loop = loop

    def tick(self):

        if super(AIBotHunter, self).tick() is False or self.following_object is None:
            return


        cx = self.following_object.rect.centerx
        cy = self.following_object.rect.centery
        cz = self.following_object.z

        x = self.target_object.rect.centerx
        y = self.target_object.rect.centery
        z = self.target_object.z

        if cz == z:
            distance = math.sqrt((cx-x)**2 + (cy-y)**2)

            if distance <= self.visibility_distance:
                self.tracker.tick()
            else:
                self.router.tick()


class AIBotRandom(AIBot):

    def __init__(self, target_object: RPGObject3D, world: World3D, tick_slow_factor : int = 1):

        super(AIBotRandom, self).__init__(str(__class__), target_object, world, tick_slow_factor)

        self.valid_actions = []
        self.current_instruction = None
        self.current_instruction_ticks = 0
        self.current_instruction_duration = 0
        self.action_on_fail = AIBotRandom.INSTRUCTION_FAIL_SKIP

    def __str__(self):

        text = "{0} Bot: valid actions:{1} : current action:{2}".format(self.name, str(self.valid_actions),
                                                                        self.valid_actions[self.current_instruction_id])

        return text

    def set_instructions(self, new_instructions: list, min_duration: int = 5, max_duration: int = 10):
        self.valid_actions = new_instructions
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.next_instruction()

    def tick(self):

        if super(AIBotRandom, self).tick() is False:
            return

        # If the  instruction requires an action...
        if self.current_instruction is not None:

            self.world.move_object(self.target_object, self.current_instruction)
            success = self.target_object.has_moved()

        # If no action then success is always true
        else:
            success = True

        # If instruction succeeded...
        if success is True:
            self.current_instruction_ticks += 1
            if self.current_instruction_ticks > self.current_instruction_duration:
                self.next_instruction()

        # If the instruction failed then determine what to do next based on option
        else:
            if self.action_on_fail == AIBot.INSTRUCTION_FAIL_NOP:
                pass
            elif self.action_on_fail == AIBot.INSTRUCTION_FAIL_TICK:
                self.current_instruction_ticks += 1
                if self.current_instruction_ticks > self.current_instruction_duration:
                    self.next_instruction()
            elif self.action_on_fail == AIBot.INSTRUCTION_FAIL_SKIP:
                self.next_instruction()

    def next_instruction(self):
        self.current_instruction = random.choice(self.valid_actions)
        self.current_instruction_ticks = 0
        self.current_instruction_duration = random.randint(self.min_duration, self.max_duration)
