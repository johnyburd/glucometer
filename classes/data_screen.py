# Class for the data_screen.  Manages displaying data stored by the meter.

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from .data_manager import DataManager
from kivy.properties import BooleanProperty
from kivy.lang import Builder

Builder.load_file('kvfiles/data_screen.kv')

class DeleteDialoguePopup(Popup):

    def __init__(self, ent, **kwargs):
        super(DeleteDialoguePopup, self).__init__(**kwargs)
        self.entry = ent
    def delete(self):
        self.entry.delete()

class DateRow(BoxLayout):

    def __init__(self, date, **kwargs):
        super(DateRow, self).__init__(**kwargs)
        dm = DataManager()
        dateobj = dm.str_to_date(date)
        self.ids.date.text = "%s %s, %s" % (dateobj.strftime('%B')[:3], dateobj.day, dateobj.year)

class EntryRow(BoxLayout):

    widths_correct = BooleanProperty(False)

    def __init__(self, date, time, b, c, bo, n, **kwargs):
        super(EntryRow, self).__init__(**kwargs)

        self.dm = DataManager()
        self.datetime = date + ' ' + time
        self.bg = b
        self.carbs = c
        self.bolus = bo
        self.notes = n

        i = self.ids
        i.time.text = time
        if b == 0:
            i.bg.text = '--'
        else:
            i.bg.text = str(b)
        if c == 0:
            i.carbs.text = '--'
        else:
            i.carbs.text = str(c)
        if bo == 0:
            i.bolus.text = '--'
        else:
            i.bolus.text = str(bo)
        i.notes.text = n

    def refresh_widths(self):
        i = self.ids
        i.bg._label.refresh()      # have to refresh to update texture size
        i.carbs._label.refresh()
        i.bolus._label.refresh()
        i.notes._label.refresh()
        i.layout.width = sum(x.width for x in self.ids.layout.children)
        totalwidth = i.layout.width + i.time.width
        print totalwidth
        if totalwidth < (Window.width + i.deletebtn.width + i.editbtn.width):
            i.spacer.width = Window.width - totalwidth + i.deletebtn.width + i.editbtn.width
            self.refresh_widths()

    def open_delete_dialogue_popup(self):
        popup = DeleteDialoguePopup(self)
        popup.open()

    def delete(self):
        self.dm.delete_entry(self.datetime, int(self.bg), int(self.carbs), int(self.bolus), self.notes)

class DataScreen(Screen):

    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)

        self.dm = DataManager()
        self.entryrows = []
        self.daterows = []
        self.render_data()

        Clock.schedule_once(self.update_row_widths, 8)
        #self.refresh()

    def render_data(self):
        layout = self.ids.layout

        rows = self.dm.get_whole_table_sorted("data")

        lastdate = ""
        rows.reverse()
        for row in rows:
            isodate = row["dateColumn"]
            isodate_split = isodate.split(' ')
            date = isodate_split[0]
            time = isodate_split[1]

            if date != lastdate:
                lastdate = date
                daterow = DateRow(date)
                layout.add_widget(daterow)
                self.daterows.append(daterow)

            bg = row['Bg']
            carbs = row['Carbs']
            bolus = row['bolus']
            notes = row['Notes']

            entry = EntryRow(date, time, bg, carbs, bolus, notes)
            layout.add_widget(entry)
            self.entryrows.append(entry)

    def refresh(self, *args):
        for entry in self.entryrows:
            self.ids.layout.remove_widget(entry)
        for date in self.daterows:
            self.ids.layout.remove_widget(date)

        self.entryrows = []
        self.render_data()
        Clock.schedule_once(self.update_row_widths, 0.5)

    def update_row_widths(self, *args):
        for entry in self.entryrows:
            entry.refresh_widths()

