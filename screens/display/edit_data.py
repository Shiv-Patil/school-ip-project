from widgets.dialog import Dialog
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.lang import Builder
import utils
import os

app = MDApp.get_running_app()

Builder.load_file(utils.get_path(os.path.join("screens", "display", "edit_data.kv")))


class EditDataContent(MDCard):
    def _on_edit_button_clicked(self):
        id = int(self.ids.id_field.text)
        if id == 0:
            return app.toast("Invalid ID")
        self.parent.parent.dismiss()
        app.root.goto("edit")
        app.root.manager.get_screen("edit")._id = str(id)


def init_editmodal(self):
    if not self.edit_dialog:
        self.edit_data_content = EditDataContent()
        self.edit_dialog = Dialog(
            auto_dismiss=True,
            content_cls=self.edit_data_content,
            overlay_color=(0, 0, 0, 0.6),
        )
