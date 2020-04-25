class Event():
    # Event Types
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
    HELP = "Help"
    COLLIDE = "collide"
    INTERACT = "interact"#
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

    def __init__(self, name: str, description: str = None, type: str = DEFAULT):
        self.name = name
        self.description = description
        self.type = type

    def __str__(self):
        return "{0}:{1} ({2})".format(self.name, self.description, self.type)