from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import utils, os
from kivy.properties import StringProperty
from kivymd.uix.datatables import MDDataTable
import pandas as pd
from kivymd.uix.menu import MDDropdownMenu
from kivy.effects.scroll import ScrollEffect
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.app import MDApp

app = MDApp.get_running_app()


class Analysis(Screen):
    _student_id = StringProperty("")
    _fullname = StringProperty("")
    _year_id = StringProperty("")
    yearmenu = None
    data_table = None
    resname = StringProperty("Total Average")
    resvalue = StringProperty("69")
    marks = None

    def on_pre_enter(self, *_args):
        if not self.yearmenu:
            self._create_dropdown()
        if not self.data_table:
            self._create_table()
        self._populate_years()

    def _populate_rows(self):
        exams = app.database.execute_query(
            "SELECT * from marks WHERE academic_year = ?", (self._year_id,)
        )

        if not isinstance(exams, list):
            return

        marks = {i[2]: i[3:] for i in exams}
        self.marks = pd.DataFrame(
            marks,
            index=("Maths", "English", "Physics", "Chemistry", "IP"),
        )
        self.resname = "Total Average"
        self.resvalue = str(round(self.marks.mean().mean(), 2)) + " %"

        row_data = (
            *zip(
                ("Mathematics", "English", "Physics", "Chemistry", "IP"),
                *(marks.get(exam) for exam in ("unit1", "term1", "unit2", "term2"))
            ),
        )

        self.data_table.update_row_data(self.data_table, row_data)

    def get_grade(self, p):
        return (
            "A1"
            if p > 90
            else "A2"
            if p > 80
            else "B1"
            if p > 70
            else "B2"
            if p > 60
            else "C1"
            if p > 50
            else "C2"
            if p > 40
            else "D"
            if p > 32
            else "E"
            if p > 0
            else "Not graded"
        )

    def _populate_years(self):
        years = app.database.execute_query(
            "SELECT * from academic_year WHERE student = ?", (self._student_id,)
        )

        if not isinstance(years, list):
            return app.root.goback()

        def set_item(text_item, yearid):
            Clock.schedule_once(lambda dt: self.yearmenu.dismiss(), 0.169)
            Clock.schedule_once(lambda dt: self.ids.year.set_item(text_item), 0.1)
            self._year_id = yearid
            self._populate_rows()

        set_item(str(years[0][5]), str(years[0][0]))

        menu_items = []
        for year in years:
            menu_items.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": str(year[5]),
                    "height": dp(52),
                    "on_release": lambda x=str(year[5]), y=str(year[0]): set_item(x, y),
                }
            )

        self.yearmenu.items = menu_items

    def _create_dropdown(self):
        if self.manager.has_screen("visualisation"):
            scrn = app.root.manager.get_screen("visualisation")
            if scrn.yearmenu:
                self.yearmenu = scrn.yearmenu
                return
        self.yearmenu = MDDropdownMenu(
            caller=self.ids.year,
            position="bottom",
            width_mult=2,
            background_color="white",
            opening_time=0,
            elevation=1,
        )
        self.yearmenu.ids.md_menu.effect_cls = ScrollEffect
        self.yearmenu.ids.md_menu.children[0].padding = (0, 0, 0, 0)

    def _create_table(self):
        self.data_table = MDDataTable(
            size_hint_max_x=dp(600),
            elevation=1,
            rows_num=5,
            effect_cls=ScrollEffect,
            column_data=[
                ("Subject", dp(30)),
                ("Unit 1", dp(20)),
                ("Term 1", dp(20)),
                ("Unit 2", dp(20)),
                ("Term 2", dp(20)),
            ],
        )

        self.data_table.ids.container.children[0].scroll_type = ["content", "bars"]
        self.data_table.ids.container.children[0].bar_width = 6
        self.data_table.ids.container.children[0].do_scroll_x = False
        self.data_table.ids.container.children[0].do_scroll_y = False
        for child in self.data_table.ids.container.children[1].ids.header.children:
            child.tooltip_text = ""
        self.data_table.ids.container.children[1].ids.first_cell.tooltip_text = ""
        self.ids.datatable_wrapper.add_widget(self.data_table)


Builder.load_file(utils.get_path(os.path.join("screens", "analysis", "analysis.kv")))
