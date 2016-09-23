from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.actionbar import ActionBar
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.progressbar import ProgressBar
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from time import localtime, strftime
import FlappyBird

#sm = ScreenManager()
            
class MainScreen(Screen):
    pass

class BGScreen(Screen):
    def start_pb(self):
        event = Clock.schedule_interval(self.update_pb, 1 / 60.)
    def update_pb(self, dt):
        self.ids.pb.value = self.ids.pb.value + (1/3.)
        if self.ids.pb.value >= 100:
            self.ids.pb.value = 0
            return False

class DataScreen(Screen):
    pass
class SettingsScreen(Screen):
    pass
class ExtrasScreen(Screen):
    pass
class HomeScreen(Screen):
    pass
class MenuBar(ActionBar):
    def __init__(self, **kwargs):

        super(MenuBar,self).__init__(**kwargs)
        self.screen_values = ['BG test', 'Data', 'Settings', 'Extras']
        self.screen_ids = ['bgtest', 'data', 'settings', 'extras']
    def set_previous(self):
        #if sm.current_screen and sm.current_screen.name == 'home':
        #    return True
        return False
    def set_time(self, dt):
        Clock.schedule_once(self.set_time, 30)

        self.ids.testid.title = strftime("%Y-%m-%d %H:%M", localtime())
        return self.ids.testid.title
    def set_screen_text(self, title):
        print title
        self.ids.spnr.text = title
    def set_screen(self):
        #sm.current = 'data'
        print(sm.current)
        for i in xrange(0,len(self.screen_values)):
            if self.screen_values[i] == self.ids.spnr.text:
                sm.transition.direction = 'left'
                sm.current = self.screen_ids[i]
                self.set_screen_text(self.screen_values[i])
                break;

class CustomScreenManager(ScreenManager):

    screen_ids = ['home','bgtest', 'data', 'settings', 'extras']
    screen_names = ['Home','BG test', 'Data', 'Settings', 'Extras']

    def __init__(self, **kwargs):

        super(CustomScreenManager,self).__init__(**kwargs)

        self.add_widget(HomeScreen(name='home'))
        self.add_widget(DataScreen(name='data'))
        self.add_widget(MainScreen(name='main'))
        self.add_widget(BGScreen(name='bgtest'))
        self.add_widget(SettingsScreen(name='settings'))
        self.add_widget(ExtrasScreen(name='extras'))

class Glucometer(App):

    test = StringProperty('test')

    screen_names = CustomScreenManager.screen_names
    screen_ids = CustomScreenManager.screen_ids

    def __init_(self, **kwargs):  # constructor is not necessary here
        super(Glucometer, self).__init__(**kwargs)

    def build(self):
        self.root.ids.spnr.text = "Home"

    def print_current_screen(self):
        return sm.current_screen.name
    def test(self):
        return StringProperty('test')
    def flappy(self):
        FlappyBird.FlappyBirdApp().run()

    def set_previous(self):
        #sm = self.root.ids.sm
        #if sm.current_screen and sm.current_screen.name == 'home':
        #    return True
        return False
    def set_time(self, dt):
        #title = self.root.ids.previousid.title
        Clock.schedule_once(self.set_time, 30)

        title = strftime("%Y-%m-%d %H:%M", localtime())
        return title
    def set_screen(self):
        sm = self.root.ids.sm
        for i in xrange(0,len(self.screen_names)):
            if self.screen_names[i] == self.root.ids.spnr.text:
                sm.transition.direction = 'left'
                sm.current = self.screen_ids[i]
                break;


Glucometer().run()
