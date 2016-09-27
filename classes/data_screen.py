
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from .data_manager import DataManager
from kivy.lang import Builder
Builder.load_file('kvfiles/DataScreen.kv')

class DataScreen(Screen):
    def __init__(self, **kwargs):
        super(DataScreen, self).__init__(**kwargs)

        self.dm = DataManager()
        rows = self.dm.get_whole_table("data")

        self.ids.layout.add_widget(Label(text="Date",text_size=(None, None), size_hint_y=None))
        self.ids.layout.add_widget(Label(text="Bg",text_size=(None, None), size_hint_y=None))
        self.ids.layout.add_widget(Label(text="Carbs",text_size=(None, None), size_hint_y=None))
        self.ids.layout.add_widget(Label(text="Bolus",text_size=(None, None), size_hint_y=None))
        self.ids.layout.add_widget(Label(text="Delete",text_size=(None, None), size_hint_y=None))
        for row in rows:

            self.ids.layout.add_widget(Label(text=str(row["Date"]),text_size=(None, None), size_hint_y=None))
            self.ids.layout.add_widget(Label(text=str(row["Bg"]),text_size=(None, None), size_hint_y=None))
            self.ids.layout.add_widget(Label(text=str(row["Carbs"]),text_size=(None, None), size_hint_y=None))
            self.ids.layout.add_widget(Label(text=str(row["Bolus"]),text_size=(None, None), size_hint_y=None))
            self.ids.layout.add_widget(Button(text="X", on_release=self.delete_row))

    def delete_row(self, row):
        self.dm.delete_entry(row)
