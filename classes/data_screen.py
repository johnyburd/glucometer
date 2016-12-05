# Class for the data_screen.  Manages displaying data stored by the meter.

from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
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

    def __init__(self, date, time, bg, carbs, bolus, notes, **kwargs):
        super(EntryRow, self).__init__(**kwargs)

        self.dm = DataManager() 
        self.datetime = date + ' ' + time

        i = self.ids
        i.time.text = time
        i.bg.text = str(bg)
        i.carbs.text = str(carbs)
        i.bolus.text = str(bolus)
        i.notes.text = notes

    def refresh_widths(self):
        i = self.ids
        i.bg._label.refresh()      # have to refresh to update texture size
        i.carbs._label.refresh()
        i.bolus._label.refresh()
        i.notes._label.refresh()
        self.ids.layout.width = sum(x.width for x in self.ids.layout.children)
        totalwidth = i.layout.width + i.time.width
        if totalwidth < (240 + i.deletebtn.width + i.editbtn.width):
            i.spacer.width = 240 - totalwidth + i.deletebtn.width + i.editbtn.width
            self.refresh_widths()

    def open_delete_dialogue_popup(self):
        popup = DeleteDialoguePopup(self)
        popup.open()

    def delete(self):
        i = self.ids
        self.dm.delete_entry(self.datetime, int(i.bg.text), int(i.carbs.text), int(i.bolus.text), i.notes.text)

class DataScreen(Screen):

    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)

        self.dm = DataManager()
        self.entryrows = []
        self.daterows = []
        self.render_data()

        Clock.schedule_once(self.update_row_widths, 2)

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
            if bg == 0:
                bg = '--'
            if carbs == 0:
                carbs = '--'
            if bolus == 0:
                bolus = '--'

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

