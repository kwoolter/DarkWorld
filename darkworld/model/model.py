import collections
import os
from darkworld.model.RPGConversations import *

from darkworld.model.worlds import *
from darkworld.model.events import *


class DWModel():
    DATA_FILES_DIR = os.path.dirname(__file__) + "\\data\\"

    # Define states
    STATE_LOADED = "Game Loaded"
    STATE_READY = "Game Ready"
    STATE_PLAYING = "Game Playing"
    STATE_PAUSED = "Game Paused"
    STATE_GAME_OVER = "Game Over"

    # Default skin name
    DEFAUL_SKIN_NAME = "default"

    # Define Effects
    EFFECT_COUNTDOWN_RATE = 20

    def __init__(self, name: str):

        # Properties
        self.name = name
        self.tick_count = 0
        self.state = DWModel.STATE_LOADED
        self._debug = False

        # Model Components
        self.events = EventQueue()
        self.world_factory = None
        self.world = None
        self.current_world_id = 0

        self.player = None
        self.player_lives = 0
        self._conversations = None
        self.effects = {}
        self.inventory = {}
        self.inventory_copy = copy.deepcopy(self.inventory)

    def initialise(self):
        print("Initialising {0}:{1}".format(self.name, __class__))

        self.world_factory = WorldBuilder(DWModel.DATA_FILES_DIR)
        self.world_factory.initialise()
        self.world_ids = self.world_factory.get_world_names()
        self.current_world_id = self.world_ids[0]
        # self.world = self.world_factory.get_world(self.current_world_id)

        self._conversations = ConversationFactory(DWModel.DATA_FILES_DIR + "conversations.xml")
        self._conversations.load()
        self._conversations.reset()

        self.player = WorldObjectLoader.get_object_copy_by_name(Objects.PLAYER)
        self.player.is_player = True
        self.player_lives = 5
        self.difficulty = 1
        self.effects = {}
        self.inventory = {}
        self.inventory_copy = copy.deepcopy(self.inventory)
        self.current_world_id = 120

        # self.move_world(self.current_world_id, do_copy=True)

        self.state = DWModel.STATE_LOADED
        self.events.add_event(Event(type=Event.STATE,
                                    name=self.state,
                                    description="Game state changed to {0}".format(self.state)))

    def reset(self):

        # Delete the player from the current world
        self.delete_world_object(self.player)

        # Restore player's inventory to what it was when we arrived in this world
        self.inventory = copy.deepcopy(self.inventory_copy)

        # Remove any effects
        self.effects = {}

        # Reset ALL conversations
        self._conversations.reset()

        # Reset the new world just for good measure
        self.world.reset()

        # Add the player to NEW copy of the current world
        self.move_world(self.current_world_id, do_copy=True)

        # Reset the new world just for good measure
        self.world.reset()

    def get_next_world_id(self):
        idx = self.world_ids.index(self.current_world_id)
        idx += 1
        if idx >= len(self.world_ids):
            idx = 0
            self.difficulty += 1
        return self.world_ids[idx]

    def get_previous_world_id(self):
        idx = self.world_ids.index(self.current_world_id)
        idx = max(idx - 1, 0)
        return self.world_ids[idx]

    def start(self):
        self.state = DWModel.STATE_PLAYING
        self.events.add_event(Event(type=Event.STATE,
                                    name=self.state,
                                    description="Game state changed to {0}".format(self.state)))

        self.move_world(self.current_world_id, do_copy=True)

    def pause(self, pause_on=None):

        if pause_on is True:
            self.state = DWModel.STATE_PAUSED
        elif pause_on is False and self.state == DWModel.STATE_PAUSED:
            self.state = DWModel.STATE_PLAYING
        elif pause_on is None:
            if self.state == DWModel.STATE_PAUSED:
                self.state = DWModel.STATE_PLAYING
            elif self.state == DWModel.STATE_PLAYING:
                self.state = DWModel.STATE_PAUSED

        self.events.add_event(Event(type=Event.STATE,
                                    name=self.state,
                                    description="Game state changed to {0}".format(self.state)))

    def print(self):

        print("Printing {0} model...".format(self.name))
        print("Game state {0}".format(self.state))
        print("Player state {0}".format(self.world.player_state))
        print("Player currently at {0}".format(self.player.xyz))
        for obj, count in self.inventory.items():
            print("Carrying {0} x {1}".format(obj, count))
        self.world.print()

    def process_event(self, new_event):
        print("Default Game event process:{0}".format(new_event))

        if new_event.type == Event.DEBUG:
            self.debug()

    def debug(self, debug_on : bool = None):

        if debug_on is None:
            self._debug = not self._debug
        else:
            self._debug = debug_on

        self.world.debug(self._debug)

    def tick(self):

        if self.state == DWModel.STATE_PLAYING:

            self.world.tick()
            self.tick_count += 1

            # See if the player is colliding with any enemies
            colliding_enemies = self.world.touching_objects(self.player, distance=0, filter=World3D.ENEMIES)

            # If you are colliding with an enemy
            if len(colliding_enemies) > 0:

                # If you are protected nothing happens
                if Event.EFFECT_PROTECTION in self.effects.keys():
                    self.events.add_event(Event(type=Event.GAME,
                                                name=Event.BLOCKED,
                                                description="You are protected"))

                # If you can kill enemies then delete them
                elif Event.EFFECT_KILL_ENEMIES in self.effects.keys():
                    for enemy in colliding_enemies:
                        if random.randint(0, 10) > 1:
                            self.swap_world_object(enemy, random.choice((Objects.TREASURE, Objects.COINS, Objects.KEY)))
                        else:
                            self.world.delete_object3D(enemy)
                    self.events.add_event(Event(type=Event.GAME,
                                                name=Event.KILL_ENEMY,
                                                description="You slay some foes"))

                # If you can kill enemies then delete them
                elif Event.EFFECT_MELEE_ATTACK in self.effects.keys():
                    for enemy in colliding_enemies:
                        if random.randint(0, 10) > 1:
                            self.swap_world_object(enemy, random.choice((Objects.TREASURE, Objects.COINS, Objects.KEY)))
                        else:
                            self.world.delete_object3D(enemy)
                    self.events.add_event(Event(type=Event.GAME,
                                                name=Event.KILL_ENEMY,
                                                description="You slay some foes"))
                # else you die
                else:
                    print("Hit enemy")
                    self.player_died()
            else:

                # Gravity tries to make the player fall
                self.world.move_player(World3D.NORTH)
                if self.world.player.has_changed_planes() is True:
                    self.world.player_state = World3D.PLAYER_FALLING
                else:
                    self.world.player_state = World3D.PLAYER_MOVING

                if self.world.is_player_dead() is True:
                    self.player_died()

            # Time to process any effects that wear off over time...
            if self.tick_count % DWModel.EFFECT_COUNTDOWN_RATE == 0:
                expired_effects = []
                for effect, count in self.effects.items():
                    if count > 0:
                        self.effects[effect] -= 1
                    elif count == 0:
                        expired_effects.append(effect)

                for effect in expired_effects:
                    del self.effects[effect]
                    self.world.remove_effect(effect)
                    self.events.add_event(Event(type=Event.GAME,
                                                name=Event.EFFECT_END,
                                                description="Effect {0} wears off!".format(effect)))

    def help(self):
        self.talk_to_npc(npc_object=None, npc_name="The Master", world_id="Help")

        n = Navigator()
        to_obj = self.player
        from_obj = self.world.bots[0].target_object

        r = n.navigate(self.world, from_obj, to_obj)
        print("{0}:{1}".format(r,n.route))


    def get_skin_name(self):
        if self.world is None:
            return DWModel.DEFAUL_SKIN_NAME
        else:
            return self.world.skin

    def get_next_event(self):
        next_event = None
        if self.events.size() > 0:
            next_event = self.events.pop_event()

        return next_event

    def move_player(self, vector):

        if self.world.player_state == World3D.PLAYER_FALLING or self.state != DWModel.STATE_PLAYING:
            return

        self.world.move_player(vector)

        ################################################
        # All collision logic moved to the tick() method
        ################################################

        # if self.world.player.has_moved() is True:
        #     pass

            # touching_objects = self.world.touching_objects(self.world.player)
            #
            # for object in touching_objects:
            #
            #     if object.name == Objects.HOLE:
            #         print("Falling...")
            #         self.move_player((0, 0, -2))
            #
            #     elif object.name == Objects.TRAP:
            #         if self.world.player.is_colliding(object):
            #             print("Ouch...")
            #             self.events.add_event(Event(type=Event.GAME,
            #                                         name=Event.LOSE_HEALTH,
            #                                         description="You hit {0}".format(object.name)))
            #
            #             self.world.delete_object3D(object)

    def talk_to_npc(self, npc_object: RPGObject3D, npc_name: str = None, world_id: str = None):

        if npc_object is not None:
            npc_id = npc_object.name
            npc_name, vanish, gift_id = self.world.get_npc_details(npc_id)
            conversation_id = "{0}:{1}".format(npc_name, self.current_world_id)
        else:
            vanish = False
            gift_id = None
            conversation_id = "{0}:{1}".format(npc_name, world_id)

        conversation = self._conversations.get_conversation(conversation_id)

        if conversation is not None:
            next_line = conversation.get_next_line()
            if next_line.attempt() is True:
                text = next_line.text
                if conversation.is_completed() is True and vanish is True:
                    if gift_id is None:
                        gift_id = Objects.EMPTY
                    self.world.swap_object(npc_object, gift_id)
                self.events.add_event(
                    Event(type=Event.GAME, name=Event.TALK, description="{0}: '{1}'".format(npc_name, text)))
            else:
                self.events.add_event(
                    Event(type=Event.GAME, name=Event.TALK,
                          description="{0} has nothing to say to you.".format(npc_name)))

        else:
            self.events.add_event(
                Event(type=Event.GAME, name=Event.TALK, description="{0} has nothing to say to you.".format(npc_name)))

    def read(self, chosen_object):

        conversation = self._conversations.get_conversation("{0}:{1}".format(chosen_object.name, self.current_world_id))
        if conversation is not None:
            next_line = conversation.get_next_line()
            if next_line.attempt() is True:
                text = next_line.text
                self.events.add_event(
                    Event(type=Event.GAME, name=Event.READ, description=text))
            else:
                self.events.add_event(
                    Event(type=Event.GAME, name=Event.ACTION_FAILED, description="Nothing to see here"))
        else:
            self.events.add_event(
                Event(type=Event.GAME, name=Event.ACTION_FAILED, description="Nothing to see here"))

    def interact(self):

        touching_objects = self.world.touching_objects(self.world.player)

        for object in touching_objects:

            if object.is_interactable is True:

                if object.name == Objects.TELEPORT:
                    if self.world.player.is_inside(object):
                        self.world.move_player_to_start()
                        self.events.add_event(Event(type=Event.GAME,
                                                    name=Event.ACTION_SUCCEEDED,
                                                    description="You activate the teleport..."))

                elif object.name == Objects.EXIT_NEXT:
                    req_obj = Objects.BOSS_KEY
                    if self.world.player.is_inside(object):
                        if self.have_inventory_object(req_obj) is True:
                            if self.move_world(self.get_next_world_id(), do_copy=True) is True:
                                # Use the boss key
                                self.use_inventory_object(req_obj)

                                # Take a snap shot of what the player has at the start of the world
                                self.inventory_copy = copy.deepcopy(self.inventory)

                                self.events.add_event(Event(type=Event.GAME,
                                                            name=Event.NEW_WORLD,
                                                            description="Welcome to {0}".format(self.world.name)))

                        else:
                            self.events.add_event(Event(type=Event.GAME,
                                                        name=Event.ACTION_FAILED,
                                                        description="You don't have {0}".format(req_obj)))

                elif object.name == Objects.EXIT_PREVIOUS:
                    if self.world.player.is_inside(object):
                        print("Going back to previous world...")
                        if self.move_world(self.get_previous_world_id()) is True:
                            self.use_inventory_object(Objects.BOSS_KEY, count=-1)
                            # Take a snap shot of what the player has at the start of the world
                            self.inventory_copy = copy.deepcopy(self.inventory)

                elif object.name == Objects.LADDER_UP:
                    self.events.add_event(Event(type=Event.GAME,
                                                name=Event.ACTION_SUCCEEDED,
                                                description="You climb up the ladder."))

                    self.world.move_player_to_start()

                elif object.name == Objects.LADDER_DOWN:
                    self.events.add_event(Event(type=Event.GAME,
                                                name=Event.ACTION_SUCCEEDED,
                                                description="You climb down the ladder."))
                    self.world.move_player(World3D.NORTH * 2)

                elif object.name == Objects.TREASURE_CHEST:
                    req_obj = Objects.KEY
                    if self.have_inventory_object(req_obj) is True:
                        print("Using {0} to open {1}...".format(req_obj, object.name))
                        self.use_inventory_object(req_obj)
                        self.swap_world_object(object, Objects.TREASURE)
                        self.events.add_event(Event(type=Event.GAME,
                                                    name=Event.TREASURE_OPEN,
                                                    description="You open the treasure chest with a key."))
                    else:
                        print("You don't have required object {0}".format(req_obj))
                        self.events.add_event(Event(type=Event.GAME,
                                                    name=Event.DOOR_LOCKED,
                                                    description="You don't have anything to open the treasure chest."))

                elif object.name == Objects.DOOR1:
                    req_obj = Objects.KEY
                    if self.have_inventory_object(req_obj) is True:
                        print("Using {0} to open {1}...".format(req_obj, object.name))
                        self.use_inventory_object(req_obj)
                        self.swap_world_object(object, Objects.DOOR1_OPEN)
                        self.events.add_event(Event(type=Event.GAME,
                                                    name=Event.DOOR_OPEN,
                                                    description="You open the door with a key."))
                    else:
                        print("You don't have required object {0}".format(req_obj))
                        self.events.add_event(Event(type=Event.GAME,
                                                    name=Event.DOOR_LOCKED,
                                                    description="You don't have anything to open the door."))

                elif object.name == Objects.DOOR2:
                    req_obj = Objects.KEY
                    if self.have_inventory_object(req_obj) is True:
                        print("Using {0} to open {1}...".format(req_obj, object.name))
                        self.use_inventory_object(req_obj)
                        self.swap_world_object(object, Objects.DOOR2_OPEN)
                        self.events.add_event(Event(type=Event.GAME,
                                                    name=Event.DOOR_OPEN,
                                                    description="You open the door with a key."))
                    else:
                        # print("You don't have required object {0}".format(req_obj))
                        self.events.add_event(Event(type=Event.GAME,
                                                    name=Event.DOOR_LOCKED,
                                                    description="You don't have anything to open the door."))


                elif object.name == Objects.TRAP_DOOR:
                    req_obj = Objects.KEY
                    if self.have_inventory_object(req_obj) is True:
                        print("Using {0} to open {1}...".format(req_obj, object.name))
                        self.use_inventory_object(req_obj)
                        x,y,z = object.xyz
                        objs_below = self.world.get_objects_at(x,y,z+1)
                        for obj in objs_below:
                            self.swap_world_object(obj, Objects.HOLE)

                        self.swap_world_object(object, Objects.EMPTY)
                        self.events.add_event(Event(type=Event.GAME,
                                                    name=Event.DOOR_OPEN,
                                                    description="You open the trap door with a key."))
                    else:
                        # print("You don't have required object {0}".format(req_obj))
                        self.events.add_event(Event(type=Event.GAME,
                                                    name=Event.DOOR_LOCKED,
                                                    description="You don't have anything to open the trap door."))

                elif object.name == Objects.TRAP:
                    req_obj = Objects.TRAP_DISABLE
                    if self.have_inventory_object(req_obj) is True:
                        self.use_inventory_object(req_obj)
                        self.delete_world_object(object)
                        self.events.add_event(Event(type=Event.GAME,
                                                    name=Event.ACTION_SUCCEEDED,
                                                    description="You disabled the trap."))
                    else:
                        self.events.add_event(Event(type=Event.GAME,
                                                    name=Event.ACTION_FAILED,
                                                    description="You don't have {0}".format(req_obj)))

                elif object.is_switch is True:
                    self.world.set_switch_object(object)
                    self.events.add_event(Event(type=Event.GAME,
                                                name=Event.SWITCH,
                                                description="You switch {0}".format(object.name)))

                elif object.name in (Objects.NPC1, Objects.NPC2):
                    self.talk_to_npc(object)

                elif object.name in (Objects.SIGN_1, Objects.SIGN_2):
                    self.read(object)

                # Temp logic
                elif object.name in Objects.EFFECT_OBJECTS.keys():
                    effect = Objects.EFFECT_OBJECTS[object.name]
                    self.add_effect(effect)
                    self.delete_world_object(object)

                else:
                    self.collect_inventory_object(object)
                    self.delete_world_object(object)
                    self.events.add_event(Event(type=Event.GAME,
                                                name=Event.ACTION_SUCCEEDED,
                                                description="You found {0}".format(object.name)))

                    if object.name == Objects.EXTRA_LIFE:
                        self.player_lives += 1

            else:
                print("Object {0} is not interactable".format(object))

    def collect_inventory_object(self, new_object):
        if new_object.is_collectable is True:
            if new_object.name not in self.inventory.keys():
                self.inventory[new_object.name] = 0
            self.inventory[new_object.name] += 1

    def do_melee_attack(self):
        self.add_effect(Event.EFFECT_MELEE_ATTACK, skip_on_dupe=True)

    def have_inventory_object(self, object_name: str):
        have = False

        if object_name in self.inventory.keys() and self.inventory[object_name] > 0:
            have = True

        return have

    def use_inventory_object(self, object_name: str, count=1):
        if object_name in self.inventory.keys():
            self.inventory[object_name] -= count

            if self.inventory[object_name] <= 0:
                del self.inventory[object_name]

        else:
            self.inventory[object_name] = -count

    def add_effect(self, effect_type: str, effect_count: int = None, skip_on_dupe : bool = False):

        if effect_type in self.effects.keys() and skip_on_dupe is True:
            print("Effect {0} already active for another {1} ticks.".format(effect_type, self.effects[effect_type]))
            return

        if effect_count is None:
            effect_count = Event.EFFECT_DURATION[effect_type]

        if effect_count > 0:
            self.effects[effect_type] = effect_count

        self.world.add_effect(effect_type, one_off=(effect_count < 1))

        self.events.add_event(Event(type=Event.GAME,
                                    name=Event.EFFECT_START,
                                    description="Effect {0} activated".format(effect_type)))

    def delete_world_object(self, old_object):
        self.world.delete_object3D(old_object)

    def player_died(self):

        self.events.add_event(Event(type=Event.GAME,
                                    name=Event.DEAD,
                                    description="{0} has died".format(self.player.name)))

        self.reset()

        self.player_lives -= 1

        if self.player_lives <= 0:
            self.state = DWModel.STATE_GAME_OVER
            self.events.add_event(Event(type=Event.STATE,
                                        name=self.state,
                                        description="{0} has died. Game Over".format(self.player.name)))
        else:
            self.state = DWModel.STATE_READY
            self.events.add_event(Event(type=Event.STATE,
                                        name=self.state,
                                        description="{0} has died.".format(self.player.name)))

    def swap_world_object(self, old_object, new_object_name):
        self.world.swap_object(old_object, new_object_name)

    def move_world(self, new_world_id: int = None, do_copy: bool = False):

        moved = False
        if new_world_id is None:
            new_world_id = self.get_next_world_id()

        print("Moving from world {0} to world {1}".format(self.current_world_id, new_world_id))

        # if self.current_world_id == new_world_id:
        #     return

        new_world = self.world_factory.get_world(new_world_id, do_copy)

        if new_world is not None:

            if self.world is not None:
                self.world.delete_player()

            self.world = new_world
            self.world.add_player(self.player, start_pos=(self.current_world_id <= new_world_id))
            self.current_world_id = new_world_id
            moved = True

            # self.events.add_event(Event(type=Event.GAME,
            #                             name=Event.NEW_WORLD,
            #                             description="Welcome to {0}".format(self.world.name)))

        else:
            print("Can't find new world {0}".format(new_world_id))

        return moved

    def get_conversation(self, npc_name: str):
        return self._conversations.get_conversation(npc_name)

    def end(self):
        print("Ending {0}".format(__class__))


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
