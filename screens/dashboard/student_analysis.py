from widgets.dialog import Dialog
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.lang import Builder
import utils
import os

app = MDApp.get_running_app()

Builder.load_file(
    utils.get_path(os.path.join("screens", "dashboard", "student_analysis.kv"))
)


class StudentAnalysisContent(MDCard):
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
            app.root.goto("student_analysis")
            student_analysis = app.root.manager.get_screen("student_analysis")
            student_analysis._student_id = str(_id)
            student_analysis._fullname = fullname
            return
        app.toast("ID does not exist")


def init_studentanalysismodal(self):
    if not self.student_analysis_dialog:
        self.student_analysis_content = StudentAnalysisContent()
        self.student_analysis_dialog = Dialog(
            auto_dismiss=True,
            content_cls=self.student_analysis_content,
            overlay_color=(0, 0, 0, 0.6),
        )
