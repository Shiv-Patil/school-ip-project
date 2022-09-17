from kivymd.uix.screen import MDScreen
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
from . import add_year, delete_year

app = MDApp.get_running_app()


class Edit(MDScreen):
    _id = StringProperty("")
    year_content = ObjectProperty()
    control = ObjectProperty()
    add_dialog = None
    delete_year_dialog = None
    years = {}
    current_year_id = None

    def on_pre_enter(self, *_args):
        if self.year_content:
            self.ids.content.remove_widget(self.year_content)

    def on_enter(self, *_args):
        self.populate_data_if_exists()
        add_year.init_addmodal(self)
        delete_year.init_deleteyearmodal(self)

    def on_leave(self, *_args):
        self.clean_screen()

    def clean_screen(self):
        self.ids.years_container.clear_widgets()
        self.ids.fname_field.text = ""
        self.ids.mname_field.text = ""
        self.ids.lname_field.text = ""

    def _on_add_button_pressed(self):
        if len(self.years) < 14:
            self.add_dialog.open()
        else:
            app.toast("Maximum number of years reached")

    def _on_delete_button_pressed(self):
        if len(self.years) < 2:
            return app.toast("Cannot delete last year")
        self.delete_year_dialog.open()

    def populate_data_if_exists(self):
        if not self._id:
            return

        student = app.database.execute_query(
            "SELECT * FROM students WHERE id = ?", (self._id,)
        )
        if not isinstance(student, list) or not student:
            return

        student = student[0]
        self.ids.fname_field.text = student[1]
        self.ids.mname_field.text = student[2]
        self.ids.lname_field.text = student[3]

        _years = app.database.execute_query(
            "SELECT * FROM academic_year WHERE student = ?", (self._id,)
        )[:14]

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
                self.years[year[5]].update({exam[2]: exam[3:]})

            _children.append(MDSegmentedControlItem(text=str(year[5])))

        self.control = MDSegmentedControl(*_children)
        self.control.bind(on_active=self.select_year)
        self.ids.years_container.add_widget(self.control)
        self.select_year(self.control, _children[0])

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

        year = self.years.get(int(yearitem.text))
        self.current_year_id = year.get("id")

        self.year_content.ids.std_field.text = year.get("class")
        self.year_content.ids.div_field.text = year.get("division")
        self.year_content.ids.rollno_field.text = year.get("rollno")
        self.year_content.ids.unit1_marks.marks = year.get("unit1")
        self.year_content.ids.unit2_marks.marks = year.get("unit2")
        self.year_content.ids.term1_marks.marks = year.get("term1")
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
