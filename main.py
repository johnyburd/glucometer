from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.actionbar import ActionBar
from kivy.properties import StringProperty
import FlappyBird

class MainScreen(Screen):
    pass

class BGScreen(Screen):
    pass

class DataScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ExtrasScreen(Screen):
    pass
class MenuBar(ActionBar):
    def set_previous(self):
        if sm.current_screen and sm.current_screen.name == 'main':
            return True
        return False


kvfile = Builder.load_file("glucometer.kv")

sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(BGScreen(name='bgtest'))
sm.add_widget(DataScreen(name='data'))
sm.add_widget(SettingsScreen(name='settings'))
sm.add_widget(ExtrasScreen(name='extras'))

class Glucometer(App):

    test = StringProperty('test')

    def build(self):
        return sm

    def print_current_screen(self):
        return sm.current_screen.name
    def test(self):
        return StringProperty('test')
    def Flappy(self):
        FlappyBird.FlappyBirdApp().run()


Glucometer().run()
