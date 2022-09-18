from widgets.dialog import Dialog
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivy.lang import Builder
import utils
import os

app = MDApp.get_running_app()

Builder.load_file(utils.get_path(os.path.join("screens", "edit", "add_year.kv")))


class AddYearContent(MDCard):
    def _on_add_button_clicked(self):
        year = int(self.ids.year_field.text)
        std = self.ids.class_field.text
        div = self.ids.div_field.text
        rollno = int(self.ids.rollno_field.text)
        if year in self.edit_screen.years:
            return app.toast("This year already exists")
        if rollno == 0:
            return app.toast("Roll number can't be 0")

        if not isinstance(
            app.database.execute_query(
                "SELECT * FROM students WHERE id = ?", (self.edit_screen._id,)
            ),
            list,
        ):
            if not app.database.execute_query(
                "INSERT INTO students VALUES (?, ?, ?, ?)",
                (self.edit_screen._id, *self.fullname),
            ):
                return app.toast("Error adding student")

        if not app.database.execute_query(
            "INSERT INTO academic_year (student, class, division, rollno, year_start) VALUES (?, ?, ?, ?, ?)",
            (self.edit_screen._id, std, div, rollno, year),
        ):
            return app.toast("Error adding year")

        _id = app.database.execute_query(
            "SELECT id FROM academic_year WHERE student = ? AND year_start = ?",
            (self.edit_screen._id, year),
        )[0][0]
        for exam in ("unit1", "unit2", "term1", "term2"):
            app.database.execute_query(
                "INSERT INTO marks (academic_year, exam, mathematics, english, phyiscs, chemistry, informatics_practices) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (_id, exam, None, None, None, None, None),
            )

        self.parent.parent.dismiss()
        self.edit_screen.clean_screen()
        self.edit_screen.populate_data_if_exists()


def init_addmodal(self):
    if not self.add_dialog:
        self.add_year_content = AddYearContent()
        self.add_year_content.edit_screen = self
        self.add_dialog = Dialog(
            auto_dismiss=True,
            content_cls=self.add_year_content,
            overlay_color=(0, 0, 0, 0.6),
        )
