from kivymd.uix.textfield import MDTextField
from kivy.properties import NumericProperty
from kivy.factory import Factory


class LimitingTextField(MDTextField):
    max_chars = NumericProperty(6)

    def insert_text(self, substring, from_undo=False):
        if len(self.text) < self.max_chars:
            return super().insert_text(substring, from_undo=from_undo)


Factory.register("LimitingTextField", LimitingTextField)
