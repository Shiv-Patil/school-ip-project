from widgets.dialog import Dialog
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.lang import Builder
import utils
import os

app = MDApp.get_running_app()

Builder.load_file(utils.get_path(os.path.join("screens", "display", "delete_data.kv")))


class DeleteDataConfirmation(MDCard):
    def _on_delete_button_clicked(self):
        entries = app.database.execute_query("SELECT Count(*) FROM academic_year")
        if not isinstance(entries, list) or entries[0][0] == 0:
            self.parent.parent.dismiss()
            return app.toast("No data to delete")

        tables = app.database.execute_query(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )

        def _after(res):
            self.parent.parent.dismiss()
            app.toast("Deleted all data")
            app.database._create_tables()

        app.start_task(lambda: self.delete_all_tables(tables), _after)

    def delete_all_tables(self, tables):
        for table in tables:
            app.database.execute_query("DROP TABLE IF EXISTS " + table[0])


def init_deletemodal(self):
    if not self.delete_dialog:
        self.delete_data_container = DeleteDataConfirmation()
        self.delete_dialog = Dialog(
            auto_dismiss=True,
            content_cls=self.delete_data_container,
            overlay_color=(0, 0, 0, 0.6),
        )
