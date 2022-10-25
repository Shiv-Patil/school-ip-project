from widgets.dialog import Dialog
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.properties import StringProperty
import utils
import os

app = MDApp.get_running_app()

Builder.load_file(utils.get_path(os.path.join("screens", "dashboard", "analysis.kv")))


class AnalysisContent(MDCard):
    action = StringProperty("Analysis")

    def _on_proceed_button_clicked(self):
        _id = int(self.ids.id_field.text.strip())
        student = app.database.execute_query(
            "SELECT * FROM students where id = ?", (_id,)
        )
        if isinstance(
            student,
            list,
        ):
            self.parent.parent.dismiss()
            fullname = student[0][1] + " " + student[0][2] + " " + student[0][3]
            app.root.goto("analysis" if self.action == "Analysis" else "visualisation")
            scrn = app.root.manager.get_screen(
                "analysis" if self.action == "Analysis" else "visualisation"
            )
            scrn._student_id = str(_id)
            scrn._fullname = fullname
            return
        app.toast("ID does not exist")


def init_analysismodal(self):
    if not self.analysis_dialog:
        self.analysis_content = AnalysisContent()
        self.analysis_dialog = Dialog(
            auto_dismiss=True,
            content_cls=self.analysis_content,
            overlay_color=(0, 0, 0, 0.6),
        )
