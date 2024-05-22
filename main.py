import re

from kivy.core.audio import SoundLoader

from platform_features import WindowsFeature
from kivy.config import Config
from win32api import GetMonitorInfo, MonitorFromPoint
monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
work_area = monitor_info.get("Work")

Config.set('graphics', 'resizable', False)
Config.set("graphics", "width", 400)
Config.set("graphics", "height", 600)
Config.set("graphics", "borderless", '0')
Config.set("graphics", "always_on_top", '1')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', work_area[2] - Config.getint("graphics", "width"))
Config.set('graphics', 'top',  work_area[3] - Config.getint("graphics", "height"))



Config.write()


from kivy.core.window import Window
import darkdetect
from kivy.animation import Animation
from kivy.clock import mainthread
import tts
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.chip import MDChip, MDChipText, MDChipLeadingIcon
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from mind import Mind


class ChatScreen(MDScreen):
        pass


class SettingsScreen(MDScreen):
    pass


class WindowManager(ScreenManager):
    pass


class App(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark" if darkdetect.isDark() else "Light"
        self.theme_cls.path_to_wallpaper = WindowsFeature().get_wallpaper_path()
        self.theme_cls.dynamic_color = True
        self.theme_cls.set_colors()
        self.mind = Mind()
        self.mind.set_trigger(self.update_messages_list)
        self.title = "Автопилот"
        self.icon = "res/anim/idle.gif"

        return Builder.load_file('main.kv')

    ### Колбеки
    def on_send_button(self):
        message = self.root.get_screen('chat_screen').ids.text_field.text
        self.mind.request(message=message)
        self.root.get_screen('chat_screen').ids.text_field.text = ""

    def on_text_changed(self):
        self.root.get_screen('chat_screen').ids.send_button.disabled = not bool(
            self.root.get_screen('chat_screen').ids.text_field.text)

    @mainthread
    def update_messages_list(self):
        self.root.get_screen('chat_screen').ids.message_list.clear_widgets()
        for mes in self.mind.messages:
            self.add_message(mes['role'] == 'user', mes['content'])
        if self.mind.status == "thinking":
            self.root.get_screen('chat_screen').ids.animation.opacity = 0
            anim = Animation(opacity=1, duration=.3)
            anim.start(self.root.get_screen('chat_screen').ids.animation)
            self.root.get_screen('chat_screen').ids.animation.source = "res/anim/thinking.zip"
            self.root.get_screen('chat_screen').ids.animation.anim_loop = 0
        else:
            self.root.get_screen('chat_screen').ids.animation.opacity = 0
            anim = Animation(opacity=1, duration=.3)
            anim.start(self.root.get_screen('chat_screen').ids.animation)
            self.root.get_screen('chat_screen').ids.animation.source = "res/anim/idle.zip"
            self.root.get_screen('chat_screen').ids.animation.anim_loop = 0

    def add_message(self, from_user: bool, message):
        pattern_code = r"<python>(.*?)</python>"
        match = re.search(pattern_code, message, re.DOTALL)
        code = None
        if match:
            code = match.group(1)
        if code is not None:
            message = message.replace(f"<python>{code}</python>", "")

        if message is not None and "init" in message:
            return
        w = MDBoxLayout(
            orientation="vertical", adaptive_height=True, spacing="8dp", padding="8dp"
        )
        w.add_widget(MDLabel(text="Вы" if from_user else "Бот", adaptive_height=True))
        #if not from_user:
            #path = tts.synth(message)
            #sound = SoundLoader.load(path)
            #sound.play()
        w.add_widget(MDLabel(text=message, adaptive_height=True))

        if (code is not None):
            w.add_widget(MDChip(
                    MDChipText(
                        text="Python"
                    ),
                    MDChipLeadingIcon(icon="python")
                ))

        self.root.get_screen('chat_screen').ids.message_list.add_widget(w)


App().run()
