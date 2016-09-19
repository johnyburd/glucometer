from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.actionbar import ActionBar
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import StringProperty
from time import gmtime, strftime
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
class HomeScreen(Screen):
    pass
class MenuBar(ActionBar):
    def set_previous(self):
        if sm.current_screen and sm.current_screen.name == 'home':
            return True
        return False
    def get_time(self):
       return strftime("%Y-%m-%d %H:%M", gmtime())


class CustomDropDown(DropDown):
    pass

dropdown = CustomDropDown()
mainbutton = Button(text='Hello', size_hint=(None, None))
mainbutton.bind(on_release=dropdown.open)
dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))


kvfile = Builder.load_file("glucometer.kv")

sm = ScreenManager()

sm.add_widget(HomeScreen(name='home'))
sm.add_widget(DataScreen(name='data'))
sm.add_widget(MainScreen(name='main'))
sm.add_widget(BGScreen(name='bgtest'))
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
    def flappy(self):
        FlappyBird.FlappyBirdApp().run()
    def opendropdown(self):
        dropdown.open


Glucometer().run()
