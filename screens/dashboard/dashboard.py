from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import utils, os
from kivymd.app import MDApp
from kivy.properties import StringProperty
from . import csv_import, csv_export, student_analysis
from plyer import filechooser
from kivy.clock import mainthread

app = MDApp.get_running_app()


class Dashboard(MDScreen):
    dialog = None
    import_csv_container = None
    student_analysis_dialog = None
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
        student_analysis.init_studentanalysismodal(self)

    def _show_btn_pressed(self):
        app.root.goto("display")

    def _import_csv_btn_pressed(self):
        self.dialog.open()

    def _export_csv_btn_pressed(self):
        @mainthread
        def _save_file(file: str):
            if not file.endswith(".csv"):
                file += ".csv"
            if csv_export.export_csv(app, file):
                app.toast('Exported csv as "' + os.path.basename(file) + '"')
            else:
                app.toast("No data to export")

        app.start_task(
            lambda *args: filechooser.save_file(
                on_selection=lambda f: _save_file(f[0]),
                filters=["*.csv"],
            ),
        )

    def _student_analysis_btn_pressed(self):
        self.student_analysis_dialog.open()

    def _class_analysis_btn_pressed(self):
        pass


Builder.load_file(utils.get_path(os.path.join("screens", "dashboard", "dashboard.kv")))
