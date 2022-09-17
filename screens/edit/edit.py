from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextFieldRect
from kivy.properties import StringProperty
import utils, os


class Edit(MDScreen):
    _id = StringProperty("")

    def _on_add_button_pressed(self):
        pass


class MarksField(MDTextFieldRect):
    pass


class MarksInputContainer(MDBoxLayout):
    exam = StringProperty("")


Builder.load_file(utils.get_path(os.path.join("screens", "edit", "edit.kv")))
