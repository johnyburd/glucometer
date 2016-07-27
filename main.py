
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import FlappyBird


class MenuScreen(GridLayout):

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text='Main Menu'))
        #self.username = TextInput(multiline=False)
        #self.add_widget(self.username)

        self.btn1 = Button(text='Data', font_size=14)
        self.btn1.bind(on_press=self.callback)
        self.add_widget(self.btn1)

        self.btn2 = Button(text='Settings', font_size=14)
        self.btn2.bind(on_press=self.callback)
        self.add_widget(self.btn2)

        self.btn3 = Button(text='Extras', font_size=14)
        self.btn3.bind(on_press=self.flappy)
        self.add_widget(self.btn3)

        self.btn4 = Button(text='Shutdown', font_size=14)
        self.btn4.bind(on_press=self.restart)
        self.add_widget(self.btn4)
        #self.password = TextInput(password=True, multiline=False)
        #self.add_widget(self.password)

    def callback(self, instance):
        print('The button <%s> is being pressed' % instance.text)

    def flappy(self, instance):
        FlappyBird.FlappyBirdApp().run()
        print("test")

    def restart(self, instance):
        command = "/usr/bin/sudo /sbin/shutdown now"
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print (output)



class MyApp(App):

    def build(self):
        return MenuScreen()


if __name__ == '__main__':
    MyApp().run()
