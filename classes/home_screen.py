# Class for the home screen.  Manages quick display graphs and averages.
# -*- coding: utf-8 -*-

from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup

from kivy.uix.vkeyboard import VKeyboard
from kivy.resources import resource_find
from kivy.graphics import Color, BorderImage, Canvas
from kivy.core.image import Image

from .data_manager import DataManager
from kivy.lang import Builder
from kivy.properties import ListProperty

from math import sin
from kivy.garden.graph import Graph, MeshLinePlot
import datetime

from classes.data_manager import DataManager

Builder.load_file('kvfiles/home_screen.kv')

from kivy.core.window import Window
from kivy.uix.widget import Widget

from kivy.garden.circulardatetimepicker import CircularTimePicker
from classes.datetime_picker_popup import DatetimePickerPopup

class HomeScreen(Screen):
    def __init__(self, **kwargs):

        super(HomeScreen, self).__init__(**kwargs)

        self.dm = DataManager()

        negday = datetime.timedelta(days=-1)
        today = datetime.date.today()

        self.begindropdown = DropDown()
        self.enddropdown = DropDown()
        for index in range(200):
            displaydate = (today + (negday * index))
            year = displaydate.year
            month = displaydate.month
            day = displaydate.day

            begindatebtn = Button(text='%s/%s/%s' % (month,day,year), size_hint_y=None, height=34, id='lo')
            enddatebtn = Button(text='%s/%s/%s' % (month,day,year), size_hint_y=None, height=34, id='up')

            begindatebtn.bind(on_release=lambda begindatebtn: self.begindropdown.select(begindatebtn.text))

            enddatebtn.bind(on_release=lambda enddatebtn: self.enddropdown.select(enddatebtn.text))

            begindatebtn.bind(on_press=self.update_graph)
            enddatebtn.bind(on_press=self.update_graph)

            self.begindropdown.add_widget(begindatebtn)
            self.enddropdown.add_widget(enddatebtn)
        self.endbtn = Button(text='%s/%s/%s' % (today.month, today.day, today.year))
        self.beginbtn = Button(text='%s/%s/%s' % ((today + negday*7).month, (today + negday*7).day, (today + negday*7).year))

        self.beginbtn.bind(on_release=self.begindropdown.open)
        self.endbtn.bind(on_release=self.enddropdown.open)
        #self.beginbtn.bind(on_text=self.update_graph)
        #self.endbtn.bind(on_text=self.update_grapt)

        self.begindropdown.bind(on_select=lambda instance, x: setattr(self.beginbtn, 'text', x))
        self.enddropdown.bind(on_select=lambda instance, x: setattr(self.endbtn, 'text', x))
        self.ids.dateselectid.add_widget(self.beginbtn)
        self.ids.dateselectid.add_widget(Label(text='-', font_size=15,size_hint_x= 0.2))
        self.ids.dateselectid.add_widget(self.endbtn)


        self.update_graph(Button(text='fakeinstance'))

    def update_graph(self,instance):
        ids = self.ids
        if str(instance.id) == 'up':  # determine upper/lower bounds
            upper_bound = self.dm.str_to_date(instance.text)
            lower_bound = self.dm.str_to_date(self.beginbtn.text)
        elif str(instance.id) == 'lo':
            upper_bound = self.dm.str_to_date(self.endbtn.text)
            lower_bound = self.dm.str_to_date(instance.text)
        else:
            upper_bound = self.dm.str_to_date(self.endbtn.text)
            lower_bound = self.dm.str_to_date(self.beginbtn.text)

        if lower_bound.day >= 10:
            ids.graphid.xmin = int(str(lower_bound.month) + str(lower_bound.day))
        else:
            ids.graphid.xmin = int(str(lower_bound.month) + '0' + str(lower_bound.day))
        if upper_bound.day >= 10:
            ids.graphid.xmax = int(str(upper_bound.month) + str(upper_bound.day))
        else:
            ids.graphid.xmax = int(str(upper_bound.month) + '0' + str(upper_bound.day))


        print ids.graphid.xmax
        print ids.graphid.xmin
        plot = MeshLinePlot(color=[.1, .7, 1, 1])
        #plot.points = [(x, 30*sin(x / 10.)+100+(x)) for x in range(0, 101)]
        rows = self.dm.get_whole_table("data")
        result = []
        carbavg = 0
        bgavg = 0
        dev = 0
        for row in rows:
            date = self.dm.str_to_date(row["dateColumn"])
            if date >= lower_bound and date <= upper_bound:
                carbavg += row["Carbs"]
                bgavg += row["Bg"]
                dev = 10
                result.append(row)
        rows = result
        if len(rows) > 0:
            ids.average_lbl.text = str(bgavg/len(rows))
            ids.deviation_lbl.text = "±" + str(dev/len(rows))
            ids.carbs_lbl.text = str(carbavg/len(rows))



        #plot.points =[(int(str(self.dm.str_to_date(row["Date"]).month)+str(self.dm.str_to_date(row["Date"]).day)), row["Bg"]) for row in rows]
        for row in rows:
            date = self.dm.str_to_date(row["dateColumn"])
            if date.day >= 10:
                dateint = int(str(date.month)+str(date.day))
            else:
                dateint = int(str(date.month) + '0' + str(date.day))
            point = (dateint, row["Bg"])
            plot.points.append(point)

        ids.graphid.add_plot(plot)
    def test_keyboard(self):

       from kivy.base import runTouchApp
       #runTouchApp(MyKeyboardListener())
       mykeyboard = MyKeyboardListener()
    def open_datetime_picker_popup(self):
        popup = DatetimePickerPopup()
        popup.open()
    def open_time_chooser_popup(self):
        popup = TimeChooserPopup()
        popup.open()
class TimeChooserPopup(Popup):
	def __init__(self, **kwargs):
		super(TimeChooserPopup, self).__init__(**kwargs)

class MyKeyboardListener(Widget):
    def __init__(self, **kwargs):
        VKeyboard.draw_keys = draw_keys_improved # replaces library's function with one below that has a larger font size
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            vkeyboard = self._keyboard.widget
            print type(vkeyboard)
            print type(self._keyboard)
            vkeyboard.layout = 'numeric.json'
            vkeyboard.height = 350
            #vkeyboard.font_size = 500
            print vkeyboard.height
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        print self.size

    def _keyboard_closed(self):
        print('My keyboard has been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('The key', keycode, 'has been pressed')
        print(' - text is %r' % text)
        print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        print keyboard
        print type(keyboard)
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

def draw_keys_improved(self):
    layout = self.available_layouts[self.layout]
    layout_rows = layout['rows']
    layout_geometry = self.layout_geometry
    layout_mode = self.layout_mode

    # draw background
    w, h = self.size

    background = resource_find(self.background_disabled
                                if self.disabled else
                                self.background)
    texture = Image(background, mipmap=True).texture
    self.background_key_layer.clear()
    with self.background_key_layer:
        Color(*self.background_color)
        BorderImage(texture=texture, size=self.size,
                    border=self.background_border)

    # XXX separate drawing the keys and the fonts to avoid
    # XXX reloading the texture each time

    # first draw keys without the font
    key_normal = resource_find(self.key_background_disabled_normal
                                if self.disabled else
                                self.key_background_normal)
    texture = Image(key_normal, mipmap=True).texture
    with self.background_key_layer:
        for line_nb in range(1, layout_rows + 1):
            for pos, size in layout_geometry['LINE_%d' % line_nb]:
                    BorderImage(texture=texture, pos=pos, size=size,
                                border=self.key_border)

    # then draw the text
    # calculate font_size
    font_size = int(w) / 12
    # draw
    for line_nb in range(1, layout_rows + 1):
        key_nb = 0
        for pos, size in layout_geometry['LINE_%d' % line_nb]:
            # retrieve the relative text
            text = layout[layout_mode + '_' + str(line_nb)][key_nb][0]
            l = Label(text=text, font_size=font_size, pos=pos, size=size,
                        font_name=self.font_name)
            self.add_widget(l)
            key_nb += 1
