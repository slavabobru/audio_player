from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader
from threading import Timer
from kivy.core.window import Window
import easygui
from mutagen.mp3 import MP3


Window.size = (400, 400)

class PlayerEcsample(BoxLayout):
    slider = ObjectProperty(None)
    file_name = ObjectProperty(None)
    play = ObjectProperty(None)
    pause = ObjectProperty(None)
    stop = ObjectProperty(None)
    time = ObjectProperty(None)
    all_time = ObjectProperty(None)
    music_file = None
    sound = None
    timer = None
    seconds = 0

    def load_music(self):
        if self.timer != None:
            self.timer.cancel()
        self.music_file = easygui.fileopenbox(filetypes=["*.mp3"])
        if self.sound != None:
            self.stop_music()
            self.seconds = 0
            self.time.text = "00:00"
        if self.music_file == None:
            self.file_name.text = "Араб музыку украл"
            self.all_time.text = "00:00"
            if self.timer != None:
                self.timer.cancel()
            self.play.disabled = True
            return
        self.sound = SoundLoader.load(self.music_file)
        audio = MP3(self.music_file)
        m, s = divmod(audio.info.length + 1, 60)
        t = "%02d:%02d" % (m, s)
        self.all_time.text = t
        self.slider.max = int(audio.info.length)
        self.slider.value = 0
        self.sound.seek(0)
        self.sound.stop()
        self.play.disabled = False
        self.timer = Timer(1, self.position)
        self.file_name.text = self.sound.source

    def play_music(self):
        self.play.disabled = True
        self.pause.disabled = False
        self.stop.disabled = False
        self.sound.play()
        self.timer.start()

    def pause_music(self):
        self.timer.cancel()
        pos = self.sound.get_pos()
        self.sound.stop()
        self.slider.value = pos
        self.play.disabled = False
        self.pause.disabled = True
        self.timer = Timer(1, self.position)

    def stop_music(self):
        self.sound.stop()
        self.timer.cancel()
        self.play.disabled = False
        self.timer = Timer(1, self.position)
        self.slider.value = 0
        self.sound.seek(0)
        self.stop.disabled = True
        self.pause.disabled = True

    def position(self):
        self.timer = Timer(1, self.position)
        self.slider.value = self.sound.get_pos()
        self.timer.start()
        self.seconds += 1
        self.time_format(self.seconds)
        if self.slider.value == 0:
            self.stop_music()
            self.slider.value = 0
            self.seconds = 0
            self.time_format(self.seconds)

    def music_position(self, instance):
        if self.sound != None:
            self.sound.seek(instance.value)
            self.seconds = instance.value
            self.time_format(self.seconds)

    def time_format(self, seconds):
        m, s = divmod(seconds, 60)
        t = "%02d:%02d" % (m, s)
        self.time.text = t


class PlayerApp(App):
    player = None
    def build(self):
        Window.bind(on_close = self.on_request_close)
        self.player = PlayerEcsample()
        return self.player

    def on_request_close(self, *args):
        self.player.sound.stop()
        self.player.timer.cancel()


if __name__ == "__main__":
    PlayerApp().run()
