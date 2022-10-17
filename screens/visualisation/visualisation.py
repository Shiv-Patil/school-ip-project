from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivy.effects.scroll import ScrollEffect
import utils, os
from kivy.clock import Clock
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.app import MDApp

app = MDApp.get_running_app()
BARWIDTH = 0.18


class Visualisation(MDScreen):
    _student_id = StringProperty("")
    _fullname = StringProperty("")
    yearmenu = None
    marks = None

    def on_pre_enter(self, *_args):
        if not self.yearmenu:
            self._create_dropdown()
        self._populate_years()

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
            exams = app.database.execute_query(
                "SELECT * from marks WHERE academic_year = ?", (yearid,)
            )
            if not isinstance(exams, list):
                self.marks = None
                return

            marks = {i[2]: i[3:] for i in exams}
            self.marks = pd.DataFrame(
                marks,
                index=("Maths", "English", "Physics", "Chemistry", "IP"),
            ).fillna(0)

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
        if self.manager.has_screen("analysis"):
            scrn = app.root.manager.get_screen("analysis")
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

    def bar_marks_per_sub(self):
        subjects = self.marks.index
        unit1 = self.marks.unit1
        term1 = self.marks.term1
        unit2 = self.marks.unit2
        term2 = self.marks.term2
        br1 = np.arange(len(unit1))
        br2 = [x + BARWIDTH for x in br1]
        br3 = [x + BARWIDTH for x in br2]
        br4 = [x + BARWIDTH for x in br3]
        plt.bar(
            br1,
            unit1,
            color="#599ad3",
            width=BARWIDTH,
            edgecolor="grey",
            label="unit 1",
        )
        plt.bar(
            br2,
            term1,
            color="#f9a65a",
            width=BARWIDTH,
            edgecolor="grey",
            label="term 1",
        )
        plt.bar(
            br3,
            unit2,
            color="#9e66ab",
            width=BARWIDTH,
            edgecolor="grey",
            label="unit 2",
        )
        plt.bar(
            br4,
            term2,
            color="#cd7058",
            width=BARWIDTH,
            edgecolor="grey",
            label="term 2",
        )
        plt.xticks([r + 1.5 * BARWIDTH for r in range(len(unit1))], subjects)
        plt.yticks(np.arange(0, 101, 5))
        plt.legend()
        plt.grid(axis="y", linestyle="-")

        def showplot(*args):
            plt.show()
            app.root.hide_loading()

        app.root.show_loading(onopen=showplot)

    def bar_marks_vs_avg_examwise(self):
        BARWIDTH = 0.25
        exams = self.marks.columns
        marks = self.marks.mean()

        br1 = np.arange(len(exams))
        br2 = [x + BARWIDTH for x in br1]

        plt.bar(
            br1,
            marks,
            color="#599ad3",
            width=BARWIDTH,
            edgecolor="grey",
            label="marks",
        )
        plt.bar(
            br2,
            marks,  # todo: get class average
            color="#f9a65a",
            width=BARWIDTH,
            edgecolor="grey",
            label="average",
        )

        plt.xticks([r + 0.5 * BARWIDTH for r in range(len(exams))], exams)
        plt.yticks(np.arange(0, 101, 5))
        plt.legend()
        plt.grid(axis="y", linestyle="-")

        def showplot(*args):
            plt.show()
            app.root.hide_loading()

        app.root.show_loading(onopen=showplot)

    def bar_marks_vs_avg_subwise(self):
        pass

    def line_perf_overall(self):
        pass

    def line_perf_subwise(self):
        pass


Builder.load_file(
    utils.get_path(os.path.join("screens", "visualisation", "visualisation.kv"))
)
