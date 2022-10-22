from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.card import MDCard
from kivy.properties import (
    StringProperty,
    ObjectProperty,
    ListProperty,
    NumericProperty,
)
import utils, os
from kivymd.app import MDApp
from kivymd.uix.segmentedcontrol.segmentedcontrol import (
    MDSegmentedControl,
    MDSegmentedControlItem,
)
from . import add_year, delete_year, delete_student

app = MDApp.get_running_app()


class Edit(Screen):
    _student_id = StringProperty("")
    year_content = ObjectProperty()
    control = ObjectProperty()
    add_dialog = None
    delete_year_dialog = None
    delete_student_dialog = None
    years = {}
    current_year_id = None
    current_year = None

    def before_enter(self):
        self.years = {}
        self.populate_data_if_exists()
        add_year.init_addmodal(self)
        delete_year.init_deleteyearmodal(self)
        delete_student.init_deletestudentmodal(self)

    def on_leave(self, *_args):
        self.ids.scrollview.scroll_y = 1
        self.clean_screen()

    def clean_screen(self):
        self.ids.years_container.clear_widgets()
        if self.year_content:
            self.ids.content.remove_widget(self.year_content)
        self.ids.fname_field.text = ""
        self.ids.mname_field.text = ""
        self.ids.lname_field.text = ""

    def _on_add_button_pressed(self):
        _fullname = self._get_fullname()
        if not _fullname:
            return
        if len(self.years) < 14:
            self.add_year_content.fullname = _fullname
            self.add_dialog.open()
        else:
            app.toast("Maximum number of years reached")

    def _on_delete_button_pressed(self):
        if len(self.years) < 2:
            return app.toast("Cannot delete last year")
        self.delete_year_dialog.open()

    def _on_deleteall_button_pressed(self):
        self.delete_student_dialog.open()

    def _on_save_button_clicked(self):
        year = self.years.get(self.current_year)
        _updated = False

        _fullname = self._get_fullname()
        if not _fullname:
            return

        std = self.year_content.ids.std_field.text.strip()
        div = self.year_content.ids.div_field.text.strip()
        rollno = self.year_content.ids.rollno_field.text.strip()
        rollno = int(rollno) if rollno else None
        if not std:
            return app.toast("Standard cannot be blank")
        if not div:
            return app.toast("Divison cannot be blank")
        if rollno is None:
            return app.toast("Roll number cannot be blank")
        if rollno == 0:
            return app.toast("Roll number cannot be 0")
        rollno = str(rollno)

        query = "UPDATE academic_year SET "
        values = []
        if not std == year.get("class"):
            query += "class = ?, "
            values.append(std)
            year["class"] = std
        if not div == year.get("division"):
            query += "division = ?, "
            values.append(div)
            year["division"] = div
        if not rollno == year.get("rollno"):
            query += "rollno = ?, "
            values.append(rollno)
            year["rollno"] = rollno

        if len(values):
            app.database.execute_query(
                query[:-2] + " WHERE id = ?", (*values, self.current_year_id)
            )
            _updated = True

        for exam in ("unit1", "unit2", "term1", "term2"):
            _cur_marks = (*self.year_content.ids[exam + "_marks"].marks,)

            if not year.get(exam) == _cur_marks:
                app.database.execute_query(
                    "UPDATE marks SET mathematics = ?, english = ?, phyiscs = ?, chemistry = ?, informatics_practices = ? WHERE id = ?",
                    (*_cur_marks, year.get(exam + "_id")),
                )
                year[exam] = _cur_marks
                _updated = True

        if _updated:
            app.toast("Data Updated")
        else:
            app.toast("No changes to update")

    def _get_fullname(self):
        fname = self.ids.fname_field.text.strip().split()
        mname = self.ids.mname_field.text.strip().split()
        lname = self.ids.lname_field.text.strip().split()

        if not len(fname) == 1 or not len(mname) <= 1 or not len(lname) == 1:
            app.toast("Invalid student name")
            return False

        return (fname[0], mname[0] if mname else "", lname[0])

    def populate_data_if_exists(self):
        _btn = self.ids.deleteall_btn
        _btn.opacity = 0
        _btn.disabled = True
        if not self._student_id:
            return

        student = app.database.execute_query(
            "SELECT * FROM students WHERE id = ?", (self._student_id,)
        )
        if not isinstance(student, list) or not student:
            return

        student = student[0]
        self.ids.fname_field.text = student[1]
        self.ids.mname_field.text = student[2]
        self.ids.lname_field.text = student[3]

        _years = app.database.execute_query(
            "SELECT * FROM academic_year WHERE student = ?", (self._student_id,)
        )

        if not _years or not isinstance(_years, list):
            app.database.execute_query(
                "DELETE FROM students WHERE id = ?",
                (self._student_id,),
            )
            return

        _children = []
        self.years = {}
        for year in _years:
            self.years[year[5]] = {
                "id": year[0],
                "class": year[2],
                "division": year[3],
                "rollno": str(year[4]),
            }

            for exam in app.database.execute_query(
                "SELECT * FROM marks WHERE academic_year = ?", (year[0],)
            ):
                self.years[year[5]].update(
                    {exam[2]: exam[3:], exam[2] + "_id": exam[0]}
                )

            _children.append(MDSegmentedControlItem(text=str(year[5])))

        self.control = MDSegmentedControl(*_children)
        self.control.bind(on_active=self.select_year)
        self.ids.years_container.add_widget(self.control)
        self.select_year(self.control, _children[0])

        if len(self.years) > 0:
            _btn.opacity = 1
            _btn.disabled = False

    def select_year(self, _inst, yearitem):
        if not self.year_content:
            self.year_content = YearContainer()

        delete_btn = self.year_content.ids.delete_btn
        if len(self.years) < 2:
            delete_btn.opacity = 0
            delete_btn.disabled = True
        else:
            delete_btn.opacity = 1
            delete_btn.disabled = False

        self.current_year = int(yearitem.text)
        year = self.years.get(self.current_year)
        self.current_year_id = year.get("id")

        self.year_content.ids.std_field.text = year.get("class")
        self.year_content.ids.div_field.text = year.get("division")
        self.year_content.ids.rollno_field.text = year.get("rollno")
        self.year_content.ids.unit1_marks.marks = year.get("unit1")
        self.year_content.ids.term1_marks.marks = year.get("term1")
        self.year_content.ids.unit2_marks.marks = year.get("unit2")
        self.year_content.ids.term2_marks.marks = year.get("term2")

        if not self.year_content.parent:
            self.ids.content.add_widget(self.year_content)


class MarksField(MDTextFieldRect):
    filter = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
    max_chars = NumericProperty(6)
    bound = NumericProperty(100)

    def insert_text(self, substring, from_undo=False):
        if not substring in self.filter:
            return
        _val = int(
            self.text[: self.cursor_col] + substring + self.text[self.cursor_col :]
        )
        if from_undo or (len(self.text) < self.max_chars and not _val > 100):
            return super().insert_text(substring, from_undo=from_undo)


class MarksInputContainer(MDBoxLayout):
    exam = StringProperty("")
    marks = ListProperty([None, None, None, None, None])


class YearContainer(MDCard):
    pass


Builder.load_file(utils.get_path(os.path.join("screens", "edit", "edit.kv")))
