from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import utils, os
from kivymd.app import MDApp
from functools import partial
from . import csv_import

app = MDApp.get_running_app()


class Dashboard(MDScreen):
    dialog = None
    import_csv_container = None

    def on_enter(self, *args):
        csv_import.init_importmodal(self)

    def _show_btn_pressed(self):
        app.root.goto("display")

    def _import_csv_btn_pressed(self):
        self.dialog.open()

    def _export_csv_btn_pressed(self):
        pass

    def _student_analysis_btn_pressed(self):
        pass

    def _class_analysis_btn_pressed(self):
        pass


Builder.load_file(utils.get_path(os.path.join("screens", "dashboard", "dashboard.kv")))
