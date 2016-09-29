
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

import settings
Builder.load_file('kvfiles/settings_screen.kv')

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        settings.init()
        self.set_brightness(settings.brightness)
        super(SettingsScreen, self).__init__(**kwargs)
    def set_brightness(self, brightness):
        try:
            call(['gpio', '-g', 'mode', '18', 'pwm'])
            call(['gpio', '-g', 'pwm', '18', str(int(brightness))])
        except:
            print 'probably not running on a raspberry pi.  can\'t set brightness to ' + str(int(brightness))
    def calib_mode(self):
        print('the switch is', str(self.ids.calibswitch.active))

