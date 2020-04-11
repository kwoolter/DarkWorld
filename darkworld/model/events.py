class Event():
    # Event Types
    QUIT = "quit"
    DEFAULT = "default"
    STATE = "state"
    GAME = "game"
    WORLD = "world"

    # Event Names
    TICK = "Tick"
    PLAYING = "playing"
    COLLIDE = "collide"
    INTERACT = "interact"
    BLOCKED = "blocked"
    ACTION_FAILED = "action failed"
    DEAD = "dead"
    SECRET = "secret"
    TREASURE = "treasure"
    DOOR_OPEN = "door opened"
    DOOR_LOCKED = "door locked"
    SWITCH = "switch"
    KEY = "key"
    TELEPORT = "teleport"
    GAIN_HEALTH = "gain health"
    LOSE_HEALTH = "lose health"
    KILLED_OPPONENT = "killed opponent"
    MISSED_OPPONENT = "missed opponent"
    DAMAGE_OPPONENT = "damaged opponent"
    VICTORY = "victory"
    TALK = "talk"

    def __init__(self, name: str, description: str = None, type: str = DEFAULT):
        self.name = name
        self.description = description
        self.type = type

    def __str__(self):
        return "{0}:{1} ({2})".format(self.name, self.description, self.type)