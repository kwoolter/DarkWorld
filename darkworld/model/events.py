class Event():
    # Event Types
    DEBUG = "debug"
    QUIT = "quit"
    DEFAULT = "default"
    STATE = "state"
    GAME = "game"
    WORLD = "world"

    # Define states
    STATE_LOADED = "Game Loaded"
    STATE_READY = "Game Ready"
    STATE_PLAYING = "Game Playing"
    STATE_PAUSED = "Game Paused"
    STATE_GAME_OVER = "Game Over"

    # Event Names
    TICK = "Tick"
    EFFECT_START = "Effect Start"
    EFFECT_END = "Effect End"
    HELP = "Help"
    COLLIDE = "collide"
    KILL_ENEMY = "kill_enemy"
    INTERACT = "interact"
    READ = "read"
    BLOCKED = "blocked"
    ACTION_FAILED = "action failed"
    ACTION_SUCCEEDED = "action succeeded"
    DEAD = "dead"
    SECRET = "secret"
    TREASURE = "treasure"
    DOOR_OPEN = "door opened"
    DOOR_LOCKED = "door locked"
    NEW_WORLD = "new world"
    SWITCH = "switch"
    TREASURE_OPEN = "treasure chest open"
    KEY = "key"
    TELEPORT = "teleport"
    GAIN_HEALTH = "gain health"
    LOSE_HEALTH = "lose health"
    KILLED_OPPONENT = "killed opponent"
    MISSED_OPPONENT = "missed opponent"
    DAMAGE_OPPONENT = "damaged opponent"
    VICTORY = "victory"
    TALK = "talk"
    RANDOM_ENVIRONMENT = "random environment"

    # Effects
    EFFECT_FREEZE_ENEMIES = "**Freeze Enemies**"
    EFFECT_KILL_ENEMIES = "Slay Foes"
    EFFECT_SLOW_ENEMIES = "Slow Enemies"
    EFFECT_INVISIBLE = "**Invisibility**"
    EFFECT_PROTECTION = "**Protection**"
    EFFECT_REVEAL_SECRETS = "**Reveal Secrets**"
    EFFECT_MELEE_ATTACK = "Melee Attack"

    EFFECT_DURATION = {
        EFFECT_INVISIBLE : 20,
        EFFECT_PROTECTION : 20,
        EFFECT_FREEZE_ENEMIES : 20,
        EFFECT_SLOW_ENEMIES: 20,
        EFFECT_REVEAL_SECRETS : 0,
        EFFECT_KILL_ENEMIES : 20,
        EFFECT_MELEE_ATTACK : 5
    }

    def __init__(self, name: str, description: str = None, type: str = DEFAULT):
        self.name = name
        self.description = description
        self.type = type

    def __str__(self):
        return "{0}:{1} ({2})".format(self.name, self.description, self.type)