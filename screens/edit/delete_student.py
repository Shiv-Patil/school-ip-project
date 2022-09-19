from widgets.dialog import Dialog
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.lang import Builder
import utils
import os

app = MDApp.get_running_app()

Builder.load_file(utils.get_path(os.path.join("screens", "edit", "delete_student.kv")))


class DeleteStudentConfirmation(MDCard):
    def _on_delete_button_clicked(self):
        if not app.database.execute_query(
            "DELETE FROM students WHERE id = ?",
            (self.edit_screen._student_id,),
        ):
            return app.toast("Error deleting student")

        self.parent.parent.dismiss()
        app.toast("Deleted Successfully")

        app.root.goback()


def init_deletestudentmodal(self):
    if not self.delete_student_dialog:
        self.delete_student_container = DeleteStudentConfirmation()
        self.delete_student_container.edit_screen = self
        self.delete_student_dialog = Dialog(
            auto_dismiss=True,
            content_cls=self.delete_student_container,
            overlay_color=(0, 0, 0, 0.6),
        )
