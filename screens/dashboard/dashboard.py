from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import utils, os
from kivymd.app import MDApp
from kivy.properties import StringProperty
from . import csv_import

app = MDApp.get_running_app()


class Dashboard(MDScreen):
    dialog = None
    import_csv_container = None
    count = StringProperty("0")

    def on_pre_enter(self):
        self.update_count()

    def update_count(self):
        res = app.database.execute_query("SELECT Count(*) FROM academic_year")
        if not isinstance(res, list):
            self.count = "0"
            return
        self.count = str(res[0][0])

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
