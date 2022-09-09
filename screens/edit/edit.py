from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import utils, os


class Edit(MDScreen):
    pass


Builder.load_file(utils.get_path(os.path.join("screens", "edit", "edit.kv")))
