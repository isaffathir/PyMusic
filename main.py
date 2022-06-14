from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from screens.screens import *

class WindowManager(ScreenManager):
    pass

class PyMusic(MDApp):
    CLASSES = {
        'Play':'screens.play'
    }
    AUTORELOADER_PATHS = [
        ('.', {'recursive': True})
    ]
    KV_FILES = [
        'kv/play.kv'
    ]
    def build(self):
        self.wm = WindowManager()
        screens = [
            Play(name="play")
        ]
        for screen in screens:
            self.wm.add_widget(screen)
        return self.wm

if __name__ == '__main__':
    PyMusic().run()