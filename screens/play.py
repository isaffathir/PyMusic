import datetime
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.core.audio import Sound,SoundLoader
from kivy.properties import NumericProperty,StringProperty
from kivy.clock import Clock
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.slider import MDSlider
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
#from nativesound import SoundLoader

class Play(MDScreen):
    durasi = NumericProperty(0)
    maxdurasi = NumericProperty(0)
    data = {
        'Song':["The Walters - I Love You So","Troye Sivan - Angel Baby"]
    }
    lagu = StringProperty("assets/music/"+data['Song'][1]+".mp3")
    def __init__(self, **kw):
        Builder.load_file("kv/play.kv")
        self.sound = SoundLoader.load(self.lagu)
        self.maxdurasilagu()
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": self.data['Song'][i],
                "height": dp(56),
                "on_release": lambda x="assets/music/"+self.data['Song'][i]+".mp3": self.menu_callback(x),
             } for i in range(len(self.data['Song']))
        ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4,
            radius=[24, 24, 24, 24],
        )
        super().__init__(**kw)

    def menu_callback(self,text_item):
        #from nativesound import SoundLoader
        musik = self.sound
        text = text_item
        lagu = text_item
        
        if lagu != self.lagu:
            print("beda")
            self.lagu = text
            new = SoundLoader.load(text)
            self.menu.dismiss()
            if self.sound.state == 'play':
                self.sound.stop()
                self.sound.unload()
                self.sound = new
                self.maxdurasilagu()
                self.sound.play()
            else:
                self.sound.unload()
                self.sound = new
                self.maxdurasilagu()
                print("stop")
        else:
            print("sama")
            self.menu.dismiss()

    def callback(self, button):
        musik = self.sound
        self.menu.caller = button
        self.menu.open()

    #ALL FUNCTION
    #======= ADDONS =============
    def detikmenit(self, sec):
        val = str(datetime.timedelta(seconds = sec)).split(':')
        return f'{val[1]}:{val[2].split(".")[0]}'


    #===== CONTROL MUSIC AREA ===========

    def playmusic(self,play_controller):
        musik = self.sound
        #print(self.lagu)
        Clock.schedule_interval(self.posisidurasi, 0)
        if self.ids.slider.value != 0:
            musik.seek(self.ids.slider.value)
        if musik.state == "stop":
            musik.play()
            self.ids.play_controller.icon = "pause"
        else:
            Clock.unschedule(self.posisidurasi)
            self.ids.play_controller.icon = "play"
            musik.stop()

    def stopmusic(self,*args):
        musik = self.sound
        Clock.unschedule(self.posisidurasi)
        self.ids.play_controller.icon = "play"
        self.ids.slider.value = 0.0
        musik.stop()

    #======== SEEK FUNCTION AREA===============

    def pindahposisi(self,*args):
        musik = self.sound
        musik.seek(self.ids.slider.value)

    def releaseseek(self,*args):
        musik = self.sound
        if self.ids.slider.value != self.durasi:
            Clock.schedule_interval(self.posisidurasi, 0)
            self.pindahposisi()
        else:
            Clock.schedule_interval(self.posisidurasi, 0)

    def ontouchup(self, *args):
        Clock.unschedule(self.posisidurasi)
        self.releaseseek()

    def ontouchdown(self, *args):
        Clock.unschedule(self.posisidurasi)

    #====== INFO AND STATS =============

    def posisidurasi(self, *args):
        musik = self.sound
        self.durasi = musik.get_pos()
        if self.ids.labelpos.text == self.ids.labelmax.text:
            Clock.unschedule(self.posisidurasi)
            self.ids.play_controller.icon = "play"
            self.ids.slider.value = 0.0
            musik.stop()
            

    def maxdurasilagu(self, *args):
        musik = self.sound
        self.maxdurasi = musik.length-1

    def debugposisi(self,btn_debug):
        
        print(self.sound)
        print(self.lagu)
