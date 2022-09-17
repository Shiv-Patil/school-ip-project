from widgets.dialog import Dialog
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.lang import Builder
import utils
import os

app = MDApp.get_running_app()

Builder.load_file(utils.get_path(os.path.join("screens", "edit", "delete_year.kv")))


class DeleteYearConfirmation(MDCard):
    def _on_delete_button_clicked(self):
        if not app.database.execute_query(
            "DELETE FROM academic_year WHERE id = ?",
            (self.edit_screen.current_year_id,),
        ):
            return app.toast("Error deleting year")

        self.parent.parent.dismiss()
        app.toast("Deleted Successfully")

        self.edit_screen.clean_screen()
        self.edit_screen.populate_data_if_exists()


def init_deleteyearmodal(self):
    if not self.delete_year_dialog:
        self.delete_year_container = DeleteYearConfirmation()
        self.delete_year_container.edit_screen = self
        self.delete_year_dialog = Dialog(
            auto_dismiss=True,
            content_cls=self.delete_year_container,
            overlay_color=(0, 0, 0, 0.6),
        )
