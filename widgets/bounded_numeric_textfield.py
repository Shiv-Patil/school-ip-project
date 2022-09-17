from kivymd.uix.textfield import MDTextField
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.factory import Factory

kv = """
<BoundedNumericTextField>:
    halign: "center"
    size_hint: None, None
    height: self.minimum_height
    width: dp(120)
    pos_hint: {"center_x": 0.5}
"""
Builder.load_string(kv)


class BoundedNumericTextField(MDTextField):
    filter = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    max_chars = NumericProperty(6)
    bound = NumericProperty(100)

    def insert_text(self, substring, from_undo=False):
        if not substring in self.filter:
            return
        _val = int(
            self.text[: self.cursor_col] + substring + self.text[self.cursor_col :]
        )
        if from_undo or (len(self.text) < self.max_chars and not _val > self.bound):
            return super().insert_text(substring, from_undo=from_undo)


Factory.register("BoundedNumericTextField", BoundedNumericTextField)
