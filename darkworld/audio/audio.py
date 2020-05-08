import darkworld.model.events as model
import pygame
import os
import random


class AudioManager:
    DEFAULT_THEME = "default"

    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"
    RESOURCES_DIR_MUSIC = os.path.dirname(__file__) + "\\resources\\music\\"

    def __init__(self):

        self.sound_themes = None
        self.music_themes = None
        self.current_sound_theme = AudioManager.DEFAULT_THEME
        self.current_music_theme = AudioManager.DEFAULT_THEME

        self.sounds_cache = None
        self.current_music = None

        self.music_on = True
        self.sound_on = True
        self.music_volume = 1.0
        self.sound_volume = 1.0

    def process_event(self, new_event: model.Event):
        print("AudioManager event process:{0}".format(new_event))
        self.get_theme_sound(new_event.name, sound_theme=self.current_sound_theme)

        if new_event.type == model.Event.STATE:
            self.play_theme_music(new_event.name, music_theme=self.current_music_theme)
        elif new_event.name == model.Event.NEW_WORLD:
            pass
            #self.play_theme_music(model.Event.STATE_PLAYING, music_theme=self.current_music_theme)

    def initialise(self):

        self.sound_themes = {}
        self.sounds_cache = {}
        self.music_themes = {}

        self.load_sound_themes()
        self.load_music_themes()

        self.current_sound_theme = AudioManager.DEFAULT_THEME
        self.current_music_theme = AudioManager.DEFAULT_THEME

        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()

    def get_theme_sound(self, sound_name: str, sound_theme: str = None, play=True):

        if self.sound_on is False:
            return None

        if sound_theme is None:
            sound_theme = self.current_sound_theme

        # First check the specified sound theme exists or use the default if not specified
        if sound_theme not in self.sound_themes.keys():
            sound_theme = AudioManager.DEFAULT_THEME
            if sound_theme not in self.sound_themes.keys():
                raise Exception("Can't find sound theme {0}.")

        # Get the details of the sounds associated with this theme
        theme = self.sound_themes[sound_theme]

        # Look for the name of the sound in the specified the
        # If we can't find it swap to teh default theme
        if sound_name not in theme.keys():
            theme = self.sound_themes[AudioManager.DEFAULT_THEME]

        # If we can't find the sound anywhere then give up
        if sound_name not in theme.keys():
            raise Exception("Can't find sound '{0}' in theme '{1}'".format(sound_name, sound_theme))

        # See what file name is associated with this sound name
        sound_file_name = theme[sound_name]

        # If the result is a list of possible sound files then pick a random one
        if isinstance(sound_file_name, tuple):
            sound_file_name = random.choice(sound_file_name)

        # If we have cached this sound file before then use it
        if sound_file_name in self.sounds_cache.keys():
            sound = self.sounds_cache[sound_file_name]

        # Else load the sound from file and store it in the cache
        else:
            sound = pygame.mixer.Sound(AudioManager.RESOURCES_DIR + sound_file_name)
            self.sounds_cache[sound_file_name] = sound

        # Play the sound at the current volume level
        if play is True and sound is not None:
            sound.set_volume(self.sound_volume)
            sound.play()

        return sound

    def load_sound_themes(self):

        new_theme_name = AudioManager.DEFAULT_THEME
        new_theme = {
            model.Event.TICK: "LTTP_Menu_Cursor.wav",
            #model.Event.ACTION_FAILED: "LTTP_Error.wav",
            model.Event.ACTION_FAILED: "interface6.wav",
            model.Event.ACTION_SUCCEEDED: "metal-ringingKW.wav",
            model.Event.BLOCKED: "interface6.wav",
            model.Event.KILL_ENEMY: "Whip.ogg",
            model.Event.TREASURE: "metal_small3.wav",
            model.Event.DEAD: "LTTP_Link_Hurt.wav",
            model.Event.DOOR_OPEN: "click36.wav",
            model.Event.DOOR_LOCKED: "lockeddoor.wav",
            model.Event.EFFECT_START: "Beam.ogg",
            model.Event.EFFECT_END: "interface6.wav",
            model.Event.READ: "random4KW.wav",
            model.Event.TALK: "huh.wav",
            model.Event.TALK: ("giant2.wav", "giant4.wav", "giant5.wav"),
            model.Event.TALK: ("tribe_a.wav", "tribe_b.wav", "tribe_c.wav", "tribe_d.wav"),
            model.Event.SWITCH: "click36.wav",
            model.Event.STATE_LOADED: "clickloud.wav",
            model.Event.STATE_PLAYING: "clickloud.wav",
            model.Event.STATE_PAUSED: "LTTP_Menu_Cursor.wav",
            model.Event.STATE_WORLD_COMPLETE: "fanfare2.wav",
            model.Event.STATE_GAME_OVER: "LTTP_Link_Hurt.wav",
            model.Event.STATE_READY: "clickloud.wav",
            model.Event.NEW_WORLD: "clickloud.wav",
            model.Event.TREASURE_OPEN: "click11.wav",
            model.Event.RANDOM_ENVIRONMENT: ("bubbles.wav", "fireplace.wav", "water-wave1.wav", "water-wave2.wav",
                                             "click44.wav", "click36.wav", "smith2.wav", "raven.wav", "raven2.wav",
                                             "Mmm.ogg", "TouchOfDeath.ogg", "Stone.ogg", "dripping.wav"),
        }

        self.sound_themes[new_theme_name] = new_theme

        new_theme_name = "dungeon"
        new_theme = {
            model.Event.RANDOM_ENVIRONMENT: (
            "click44.wav", "click36.wav", "smith2.wav", "TouchOfDeath.ogg", "Stone.ogg", "dripping.wav", "drain.ogg"),
        }

        self.sound_themes[new_theme_name] = new_theme

    def load_music_themes(self):

        new_theme_name = AudioManager.DEFAULT_THEME
        new_theme = {
            model.Event.STATE_LOADED: "our-story-begins-by-kevin-macleod-from-filmmusic-io.mp3",
            model.Event.STATE_PLAYING: "dark-times-by-kevin-macleod-from-filmmusic-io.mp3",
            model.Event.STATE_PAUSED: "lost-time-by-kevin-macleod-from-filmmusic-io.mp3",
            model.Event.STATE_READY: "Ossuary 5 - Rest.mp3",
            model.Event.STATE_WORLD_COMPLETE: "the-ice-giants-by-kevin-macleod-from-filmmusic-io.mp3",
            model.Event.STATE_GAME_OVER: "the-descent-by-kevin-macleod-from-filmmusic-io.mp3",
        }

        self.music_themes[new_theme_name] = new_theme

        new_theme_name = "dungeon"
        new_theme = {

            model.Event.STATE_PLAYING: "strength-of-the-titans-by-kevin-macleod-from-filmmusic-io.mp3",

        }

        self.music_themes[new_theme_name] = new_theme

        new_theme_name = "tutorial"
        new_theme = {

            model.Event.STATE_PLAYING: "grave-matters-by-kevin-macleod-from-filmmusic-io.mp3",

        }

        self.music_themes[new_theme_name] = new_theme

    def play_theme_music(self, music_name: str, music_theme: str = None, repeat: int = 1):

        # If music is turned off stop here
        if self.music_on is False:
            return

        # If no theme specified or theme not found use default
        if music_theme is None or music_theme not in self.music_themes.keys():
            #music_theme = self.current_music_theme
            music_theme = AudioManager.DEFAULT_THEME

        print("Play that funky music...{0} from {1} theme".format(music_name, music_theme))

        theme = self.music_themes[music_theme]

        # If we can't find the specified music then look in default theme
        if music_name not in theme.keys():
            music_theme = AudioManager.DEFAULT_THEME
            theme = self.music_themes[music_theme]
            if music_name not in theme.keys():
                print("Can't find music {0} in theme {1}".format(music_name, music_theme))
                raise Exception("Can't find music {0} in theme {1}".format(music_name, music_theme))

        music_file_name = theme[music_name]

        #try:
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        self.stop_music()

        print("playing '{0}' as the {1} music for theme {2}".format(music_file_name, music_name, music_theme))
        pygame.mixer.music.load(AudioManager.RESOURCES_DIR_MUSIC + music_file_name)
        pygame.mixer.music.play(-1)

        # except Exception as err:
        #     print(str(err))

    def stop_music(self):

        pygame.mixer.music.stop()
        pygame.mixer.music.fadeout(700)

    def change_volume(self, delta: float = 0.1):
        self.music_volume += delta
        self.music_volume = max(min(self.music_volume, 1.0), 0)
        self.sound_volume += delta
        self.sound_volume = max(min(self.sound_volume, 1.0), 0)

        pygame.mixer.music.set_volume(self.music_volume)

    def end(self):
        pygame.mixer.quit()
        print("Ending {0}".format(__class__))

    def print(self):
        print("sound theme={0}  music theme={1}".format(self.current_sound_theme, self.current_music_theme))
        print("{0} sounds loaded".format(len(self.sound_themes.keys())))
        print("{0} music loaded".format(len(self.music_themes.keys())))
        print("sound={0} : music={1}".format(self.sound_on, self.music_on))
        print("sound Volume = {0}; Music Volumne = {1}".format(self.sound_volume, pygame.mixer.music.get_volume()))
