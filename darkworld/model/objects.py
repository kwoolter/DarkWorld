from .events import *


class Objects:

    BIG_MONSTER1 = "big monster1"
    BIG_MONSTER2 = "big monster2"
    BLOCK1 = "block1"
    BLOCK2 = "block2"
    BOMB = "bomb"
    BOOK = "a book"
    BOSS_KEY = "exit key"
    CRATE = "crate"
    COINS = "coins"
    DECOR1 = "decor1"
    DECOR2 = "decor2"
    DOOR1 = "door"
    DOOR1_OPEN = "door open"
    DOOR2 = "door2"
    DOOR2_OPEN = "door2 open"
    EMPTY = "empty"
    ENEMY1 = "enemy1"
    ENEMY2 = "enemy2"
    EXTRA_LIFE = "an extra life"
    EXIT_NEXT = "exit_next"
    EXIT_PREVIOUS = "exit_previous"
    FAKE_WALL = "fake wall"
    HELMET1 = "helmet1"
    HELMET2 = "helmet2"
    HOLE = "hole"
    KEY = "key"
    LADDER_DOWN = "ladder down"
    LADDER_UP = "ladder up"
    LIQUID1 = "liquid1"
    LIQUID2 = "liquid2"
    MAP = "map"
    MONSTER1 = "monster1"
    MONSTER2 = "monster2"
    NPC1 = "NPC1"
    NPC2 = "NPC2"
    PLAYER = "player"
    PLAYER2 = "player2"
    POTION1 = "potion1"
    POTION2 = "potion2"
    SCROLL = "a scroll"
    SIGN_1 = "sign 1"
    SIGN_2 = "sign 2"
    SWITCH_1 = "switch 1"
    SWITCH_2 = "switch 2"
    SWITCH_3 = "switch 3"
    SWITCH_4 = "switch 4"
    SWITCH_TILE1 = "switch tile 1"
    SWITCH_TILE2 = "switch tile 2"
    SWITCH_TILE3 = "switch tile 3"
    SWITCH_TILE4 = "switch tile 4"
    SWORD = "sword"
    TELEPORT = "teleport"
    TILE1 = "tile1"
    TILE2 = "tile2"
    TILE3 = "tile3"
    TILE4 = "tile4"
    TRAP = "trap"
    TRAP_DISABLE = "a trap disabler"
    TRAP_DOOR = "trap door"
    TREASURE = "treasure"
    TREASURE_CHEST = "treasure chest"
    WALL1 = "wall1"
    WALL2 = "wall2"
    WALL3 = "wall3"

    EFFECT_OBJECTS = {
        POTION1 : Event.EFFECT_INVISIBLE,
        SCROLL : Event.EFFECT_REVEAL_SECRETS,
        BOOK : Event.EFFECT_FREEZE_ENEMIES,
        MAP: Event.EFFECT_ITEM_DISCOVERY,
        POTION2: Event.EFFECT_SLOW_ENEMIES,
        HELMET1 : Event.EFFECT_PROTECTION,
        SWORD: Event.EFFECT_KILL_ENEMIES
    }

