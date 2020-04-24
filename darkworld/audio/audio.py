import darkworld.model.events as model
import pygame
import os

class AudioManager:

    DEFAULT_THEME = "default"
    PLAYING = model.Event.STATE_PLAYING

    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"
    RESOURCES_DIR_MUSIC = os.path.dirname(__file__) + "\\resources\\music\\"

    def __init__(self):

        self.sound_themes = None
        self.music_themes = None
        self.sounds_cache = None
        self.current_music = None
        self.music_on = True
        self.sound_on = True

    def process_event(self, new_event: model.Event):
        print("AudioManager event process:{0}".format(new_event))
        sound = self.get_theme_sound(new_event.name)
        if sound is not None:
            sound.play()

        if new_event.type == model.Event.STATE:
            self.play_theme_music(new_event.name)

    def initialise(self):

        self.sound_themes = {}
        self.sounds_cache = {}
        self.music_themes = {}

        self.load_sound_themes()
        self.load_music_themes()

        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()

    def get_theme_sound(self, sound_name: str, sound_theme: str = DEFAULT_THEME, play=True):

        sound = None

        if self.sound_on is False:
            return None

        if sound_theme not in self.sound_themes.keys():
            sound_theme = AudioManager.DEFAULT_THEME
            if sound_theme not in self.sound_themes.keys():
                raise Exception("Can't find sound theme {0}.")

        theme = self.sound_themes[sound_theme]

        if sound_name not in theme.keys():
            theme = self.sound_themes[AudioManager.DEFAULT_THEME]

        if sound_name not in theme.keys():
            raise Exception("Can't find sound '{0}' in theme '{1}'".format(sound_name, sound_theme))

        if sound_name in self.sounds_cache.keys():
            sound = self.sounds_cache[sound_name]

        else:
            sound_file_name = theme[sound_name]
            if sound_file_name is not None:
                sound = pygame.mixer.Sound(AudioManager.RESOURCES_DIR + sound_file_name)
                self.sounds_cache[sound_name] = sound
            else:
                self.sounds_cache[sound_name] = None

        if play is True and sound is not None:
            sound.play()

        return sound

    def load_sound_themes(self):

        new_theme_name = AudioManager.DEFAULT_THEME
        new_theme = {
            model.Event.TICK: "LTTP_Menu_Cursor.wav",
            model.Event.ACTION_FAILED: "LTTP_Error.wav",
            model.Event.ACTION_SUCCEEDED: "LTTP_Get_Key.wav",
            model.Event.BLOCKED: "LTTP_Error.wav",
            model.Event.STATE_PLAYING: "LTTP_Rupee1.wav",
            model.Event.TREASURE: "LTTP_Rupee1.wav",
            model.Event.DEAD: "LTTP_Link_Hurt.wav",
            model.Event.DOOR_OPEN: "click36.wav",
            model.Event.READ: "LTTP_Menu_Select.wav",
            model.Event.TALK: "huh.wav",
            model.Event.SWITCH: "click23.wav",
            model.Event.STATE_PAUSED: "LTTP_Menu_Cursor.wav",
            model.Event.STATE_GAME_OVER: "LTTP_Link_Hurt.wav",
            model.Event.STATE_READY: "LA_TrendyGame_Win.wav",
            model.Event.TREASURE_OPEN:"click11.wav",
        }

        self.sound_themes[new_theme_name] = new_theme

    def load_music_themes(self):
        new_theme_name = AudioManager.DEFAULT_THEME
        new_theme = {

            model.Event.STATE_GAME_OVER: "Rains Will Fall.mp3",
            model.Event.STATE_GAME_OVER: "the-descent-by-kevin-macleod-from-filmmusic-io.mp3",
            model.Event.STATE_READY: "our-story-begins-by-kevin-macleod-from-filmmusic-io.mp3",
            model.Event.STATE_PLAYING: "M02_Firelink Shrine.mp3",
            model.Event.STATE_PLAYING: "dark-times-by-kevin-macleod-from-filmmusic-io.mp3",
            model.Event.STATE_PAUSED: "lost-time-by-kevin-macleod-from-filmmusic-io.mp3",
        }

        self.music_themes[new_theme_name] = new_theme

        new_theme_name = "dungeon"
        new_theme = {

            model.Event.STATE_GAME_OVER: "Rains Will Fall.mp3",
            model.Event.STATE_GAME_OVER: "the-descent-by-kevin-macleod-from-filmmusic-io.mp3",
            model.Event.STATE_READY: "our-story-begins-by-kevin-macleod-from-filmmusic-io.mp3",
            model.Event.STATE_PLAYING: "M02_Firelink Shrine.mp3",
            model.Event.STATE_PLAYING: "dark-times-by-kevin-macleod-from-filmmusic-io.mp3",
            model.Event.STATE_PAUSED: "lost-time-by-kevin-macleod-from-filmmusic-io.mp3",
        }

        self.music_themes[new_theme_name] = new_theme

    def play_theme_music(self, music_name: str, music_theme: str = DEFAULT_THEME, repeat: int = 1):

        print("Play that funky music...{0} from {1} theme".format(music_name, music_theme))

        if self.music_on is False:
            return

        if music_theme not in self.music_themes.keys():
            music_theme = AudioManager.DEFAULT_THEME

        theme = self.music_themes[music_theme]

        if music_name not in theme.keys():
            raise Exception("Can't find sound {0} in theme {1}".format(music_name, music_theme))

        music_file_name = theme[music_name]

        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()

            self.stop_music()

            print("playing '{0}' as the {1} music for theme {2}".format(music_file_name, music_name, music_theme))
            pygame.mixer.music.load(AudioManager.RESOURCES_DIR_MUSIC + music_file_name)
            pygame.mixer.music.play(-1)

        except Exception as err:
            print(str(err))

    def stop_music(self):

        # pygame.mixer.music.stop()
        pygame.mixer.music.fadeout(700)

    def end(self):
        pygame.mixer.quit()


    def print(self):
        print("{0} sounds loaded".format(len(self.sound_themes.keys())))
        print("{0} music loaded".format(len(self.music_themes.keys())))
        print("sound={0} : music={1}".format(self.sound_on, self.music_on))