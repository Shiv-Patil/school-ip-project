from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivy.effects.scroll import ScrollEffect
import utils, os
from kivy.clock import Clock
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.app import MDApp

app = MDApp.get_running_app()
BARWIDTH = 0.18
plt.style.use("fivethirtyeight")


class Visualisation(Screen):
    _student_id = StringProperty("")
    _fullname = StringProperty("")
    _std_div = StringProperty("")
    _year_id = StringProperty("")
    yearmenu = None
    marks = None

    def before_enter(self):
        if not self.yearmenu:
            self._create_dropdown()
        self._populate_years()

    def _populate_years(self):
        years = app.database.execute_query(
            "SELECT * from academic_year WHERE student = ?", (self._student_id,)
        )

        if not isinstance(years, list):
            return app.root.goback()

        def set_item(text_item, yearid, std, div):
            Clock.schedule_once(lambda dt: self.yearmenu.dismiss(), 0.169)
            Clock.schedule_once(lambda dt: self.ids.year.set_item(text_item), 0.1)
            self._year_id = yearid
            self._std_div = std + " " + (div if div else "")
            exams = app.database.execute_query(
                "SELECT * from marks WHERE academic_year = ?", (yearid,)
            )
            if not isinstance(exams, list):
                self.marks = None
                return

            marks = {"unit1": (), "term1": (), "unit2": (), "term2": ()}
            for i in exams:
                marks[i[2]] = i[3:]

            self.marks = pd.DataFrame(
                marks,
                index=("Maths", "English", "Physics", "Chemistry", "IP"),
            ).fillna(value=np.nan)

        set_item(str(years[0][5]), str(years[0][0]), years[0][2], years[0][3])

        menu_items = []
        for year in years:
            menu_items.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": str(year[5]),
                    "height": dp(52),
                    "on_release": lambda x=str(year[5]), y=str(year[0]), std=year[
                        2
                    ], div=year[3]: set_item(x, y, std, div),
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

        plt.figure(num="Student marks per subject")
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

        args = app.database.execute_query(
            "SELECT class, division, year_start FROM academic_year WHERE id = ?",
            (self._year_id,),
        )[0]
        students = [
            i[0]
            for i in app.database.execute_query(
                "SELECT id FROM academic_year WHERE class = ? AND division = ? AND year_start = ?",
                args,
            )
        ]

        avgmarks = {}

        for row in app.database.execute_query(
            f"SELECT * FROM marks WHERE academic_year IN ({','.join(['?']*len(students))})",
            students,
        ):
            curr = avgmarks.get(row[2])
            next = pd.Series(row[3:]).mean()
            if not np.isnan(next) and not curr is None:
                avgmarks[row[2]].append(next)
            elif curr is None:
                avgmarks[row[2]] = []

        for _exam, _marks in list(avgmarks.items()):
            avgmarks[_exam] = round(sum(_marks) / len(_marks), 2) if len(_marks) else 0

        avgmarks = pd.Series(avgmarks)

        br1 = np.arange(len(exams))
        br2 = [x + BARWIDTH for x in br1]

        plt.figure(num="Student marks vs class average marks examwise")
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
            avgmarks,
            color="#f9a65a",
            width=BARWIDTH,
            edgecolor="grey",
            label="class average marks",
        )

        plt.xticks(np.arange(len(exams)) + BARWIDTH / 2, exams)
        plt.yticks(np.arange(0, 101, 5))
        plt.legend()
        plt.grid(axis="y", linestyle="-")

        def showplot(*args):
            plt.show()
            app.root.hide_loading()

        app.root.show_loading(onopen=showplot)

    def bar_marks_vs_avg_subwise(self):
        BARWIDTH = 0.25
        subjects = self.marks.index
        marks = self.marks.mean(axis=1)

        args = app.database.execute_query(
            "SELECT class, division, year_start FROM academic_year WHERE id = ?",
            (self._year_id,),
        )[0]
        students = [
            i[0]
            for i in app.database.execute_query(
                "SELECT id FROM academic_year WHERE class = ? AND division = ? AND year_start = ?",
                args,
            )
        ]

        avgmarks = (
            *map(
                lambda x: round(x, 2) if x else np.nan,
                app.database.execute_query(
                    f"SELECT AVG(mathematics), AVG(english), AVG(phyiscs), AVG(chemistry), AVG(informatics_practices) FROM marks WHERE academic_year IN ({','.join(['?']*len(students))})",
                    students,
                )[0],
            ),
        )

        br1 = np.arange(len(subjects))
        br2 = [x + BARWIDTH for x in br1]

        plt.figure(num="Student marks vs class average marks subjectwise")
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
            avgmarks,
            color="#f9a65a",
            width=BARWIDTH,
            edgecolor="grey",
            label="class average marks",
        )

        plt.xticks(np.arange(len(subjects)) + BARWIDTH / 2, subjects)
        plt.yticks(np.arange(0, 101, 5))
        plt.legend()
        plt.grid(axis="y", linestyle="-")

        def showplot(*args):
            plt.show()
            app.root.hide_loading()

        app.root.show_loading(onopen=showplot)

    def line_perf_overall(self):
        exams = self.marks.columns
        x = np.arange(len(exams))
        y = self.marks.mean()

        plt.figure(num="Student performance overall")
        plt.plot(x, y, "go--", linewidth=2, markersize=12)

        plt.xticks(np.arange(len(exams)), exams)

        start = max(-round(-self.marks.min().min(), -1) - 10, 0)
        if np.isnan(start):
            start = 0
        stop = min(round(self.marks.max().max(), -1) + 11, 101)
        if np.isnan(stop):
            stop = 101

        plt.yticks(
            np.arange(
                start,
                stop,
                5,
            )
        )

        plt.grid(True, axis="y", linestyle=":", which="both")
        plt.minorticks_on()
        plt.tick_params(axis="x", which="minor", bottom=False)

        def showplot(*args):
            plt.show()
            app.root.hide_loading()

        app.root.show_loading(onopen=showplot)

    def line_perf_subwise(self):
        exams = self.marks.columns
        x = np.arange(len(exams))
        maths = self.marks.iloc[0]
        eng = self.marks.iloc[1]
        phy = self.marks.iloc[2]
        chem = self.marks.iloc[3]
        ip = self.marks.iloc[4]

        plt.figure(num="Student performance subjectwise")
        plt.plot(
            x,
            maths,
            color="#599ad3",
            marker="o",
            linestyle="dashed",
            linewidth=2,
            markersize=12,
            label="Maths",
        )
        plt.plot(
            x,
            eng,
            color="#f9a65a",
            marker="o",
            linestyle="dashed",
            linewidth=2,
            markersize=12,
            label="English",
        )
        plt.plot(
            x,
            phy,
            color="#9e66ab",
            marker="o",
            linestyle="dashed",
            linewidth=2,
            markersize=12,
            label="Physics",
        )
        plt.plot(
            x,
            chem,
            color="#cd7058",
            marker="o",
            linestyle="dashed",
            linewidth=2,
            markersize=12,
            label="Chemistry",
        )
        plt.plot(
            x,
            ip,
            color="#d77fb3",
            marker="o",
            linestyle="dashed",
            linewidth=2,
            markersize=12,
            label="IP",
        )

        plt.xticks(np.arange(len(exams)), exams)

        start = max(-round(-self.marks.min().min(), -1) - 10, 0)
        if np.isnan(start):
            start = 0
        stop = min(round(self.marks.max().max(), -1) + 11, 101)
        if np.isnan(stop):
            stop = 101

        plt.yticks(
            np.arange(
                start,
                stop,
                5,
            )
        )

        plt.grid(True, axis="y", linestyle=":", which="both")
        plt.minorticks_on()
        plt.tick_params(axis="x", which="minor", bottom=False)
        plt.legend()

        def showplot(*args):
            plt.show()
            app.root.hide_loading()

        app.root.show_loading(onopen=showplot)

    def pie_class_perf_overall(self):
        fig, axes = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(12, 8))
        args = app.database.execute_query(
            "SELECT class, division, year_start FROM academic_year WHERE id = ?",
            (self._year_id,),
        )[0]
        students = [
            i[0]
            for i in app.database.execute_query(
                "SELECT id FROM academic_year WHERE class = ? AND division = ? AND year_start = ?",
                args,
            )
        ]
        buckets = dict(
            zip(
                ("unit1", "term1", "unit2", "term2", "overall"),
                map(
                    lambda d: dict(
                        zip(utils.grades.values(), (0,) * len(utils.grades))
                    ).copy(),
                    range(5),
                ),
            )
        )

        overalls = {}

        for row in app.database.execute_query(
            f"SELECT * FROM marks WHERE academic_year IN ({','.join(['?']*len(students))})",
            students,
        ):
            exam_avg = pd.Series(row[3:]).mean()
            if overalls.get(row[1], None) and not np.isnan(exam_avg):
                overalls[row[1]] = (overalls.get(row[1]) + exam_avg) / 2.0
            elif not np.isnan(exam_avg):
                overalls[row[1]] = exam_avg
            if not np.isnan(exam_avg):
                buckets[row[2]][utils.get_grade(exam_avg)] += 1

        for p in overalls.values():
            buckets["overall"][utils.get_grade(p)] += 1

        for bucket in buckets.values():
            for grade, num in list(bucket.items()):
                if num == 0:
                    del bucket[grade]

        axes[0, 0].set_title("Unit 1")
        axes[0, 0].pie(
            buckets.get("unit1").values(),
            autopct=lambda n: round(n * sum(buckets.get("unit1").values()) / 100),
            pctdistance=1.14,
            colors=[utils.pie_colors[key] for key in buckets.get("unit1").keys()],
        )

        axes[0, 1].set_title("Term 1")
        axes[0, 1].pie(
            buckets.get("term1").values(),
            autopct=lambda n: round(n * sum(buckets.get("term1").values()) / 100),
            pctdistance=1.14,
            colors=[utils.pie_colors[key] for key in buckets.get("term1").keys()],
        )

        axes[1, 0].set_title("Unit 2")
        axes[1, 0].pie(
            buckets.get("unit2").values(),
            autopct=lambda n: round(n * sum(buckets.get("unit2").values()) / 100),
            pctdistance=1.14,
            colors=[utils.pie_colors[key] for key in buckets.get("unit2").keys()],
        )

        axes[1, 1].set_title("Term 2")
        axes[1, 1].pie(
            buckets.get("term2").values(),
            autopct=lambda n: round(n * sum(buckets.get("term2").values()) / 100),
            pctdistance=1.14,
            colors=[utils.pie_colors[key] for key in buckets.get("term2").keys()],
        )
        fig.suptitle("Class performance per exam")

        patchList = []
        for key in utils.pie_colors:
            data_key = mpatches.Patch(color=utils.pie_colors[key], label=key)
            patchList.append(data_key)

        fig.legend(handles=patchList)

        plt.figure()
        plt.tight_layout(pad=0)
        plt.pie(
            buckets.get("overall").values(),
            labels=buckets.get("overall").keys(),
            labeldistance=None,
            autopct=lambda n: round(n * sum(buckets.get("overall").values()) / 100),
            pctdistance=1.14,
            colors=[utils.pie_colors[key] for key in buckets.get("overall").keys()],
        )
        plt.title("Class performance overall")
        plt.legend(bbox_to_anchor=(1.03, 1))

        def showplot(*args):
            plt.show()
            app.root.hide_loading()

        app.root.show_loading(onopen=showplot)

    def pie_class_perf_subwise(self):
        args = app.database.execute_query(
            "SELECT class, division, year_start FROM academic_year WHERE id = ?",
            (self._year_id,),
        )[0]
        students = [
            i[0]
            for i in app.database.execute_query(
                "SELECT id FROM academic_year WHERE class = ? AND division = ? AND year_start = ?",
                args,
            )
        ]
        buckets = dict(
            zip(
                ("maths", "english", "physics", "chemistry", "ip"),
                map(
                    lambda d: dict(
                        zip(utils.grades.values(), (0,) * len(utils.grades))
                    ).copy(),
                    range(5),
                ),
            )
        )

        sub_overalls = {}

        for row in app.database.execute_query(
            f"SELECT * FROM marks WHERE academic_year IN ({','.join(['?']*len(students))})",
            students,
        ):
            for sub, marks in zip(
                ("maths", "english", "physics", "chemistry", "ip"), row[3:]
            ):
                if marks:
                    if sub_overalls.get(row[1]) and sub_overalls.get(row[1]).get(sub):
                        sub_overalls[row[1]][sub].append(marks)
                        continue
                    elif not sub_overalls.get(row[1], None):
                        sub_overalls[row[1]] = {}
                    sub_overalls[row[1]][sub] = [marks]

        for student_sub_marks in sub_overalls.values():
            for sub, marks in student_sub_marks.items():
                buckets[sub][utils.get_grade(sum(marks) / len(marks))] += 1

        for bucket in buckets.values():
            for grade, num in list(bucket.items()):
                if num == 0:
                    del bucket[grade]

        plt.figure("Maths")
        plt.title("Class performance in Maths")
        plt.pie(
            buckets.get("maths").values(),
            labels=buckets.get("maths").keys(),
            labeldistance=None,
            autopct=lambda n: round(n * sum(buckets.get("maths").values()) / 100),
            pctdistance=1.14,
            colors=[utils.pie_colors[key] for key in buckets.get("maths").keys()],
        )
        plt.legend(bbox_to_anchor=(1.03, 1))

        plt.figure("English")
        plt.title("Class performance in English")
        plt.pie(
            buckets.get("english").values(),
            labels=buckets.get("english").keys(),
            labeldistance=None,
            autopct=lambda n: round(n * sum(buckets.get("english").values()) / 100),
            pctdistance=1.14,
            colors=[utils.pie_colors[key] for key in buckets.get("english").keys()],
        )
        plt.legend(bbox_to_anchor=(1.03, 1))

        plt.figure("Physics")
        plt.title("Class performance in Physics")
        plt.pie(
            buckets.get("physics").values(),
            labels=buckets.get("physics").keys(),
            labeldistance=None,
            autopct=lambda n: round(n * sum(buckets.get("physics").values()) / 100),
            pctdistance=1.14,
            colors=[utils.pie_colors[key] for key in buckets.get("physics").keys()],
        )
        plt.legend(bbox_to_anchor=(1.03, 1))

        plt.figure("Chemistry")
        plt.title("Class performance in Chemistry")
        plt.pie(
            buckets.get("chemistry").values(),
            labels=buckets.get("chemistry").keys(),
            labeldistance=None,
            autopct=lambda n: round(n * sum(buckets.get("chemistry").values()) / 100),
            pctdistance=1.14,
            colors=[utils.pie_colors[key] for key in buckets.get("chemistry").keys()],
        )
        plt.legend(bbox_to_anchor=(1.03, 1))

        plt.figure("IP")
        plt.title("Class performance in IP")
        plt.pie(
            buckets.get("ip").values(),
            labels=buckets.get("ip").keys(),
            labeldistance=None,
            autopct=lambda n: round(n * sum(buckets.get("ip").values()) / 100),
            pctdistance=1.14,
            colors=[utils.pie_colors[key] for key in buckets.get("ip").keys()],
        )
        plt.legend(bbox_to_anchor=(1.03, 1))

        def showplot(*args):
            plt.show()
            app.root.hide_loading()

        app.root.show_loading(onopen=showplot)


Builder.load_file(
    utils.get_path(os.path.join("screens", "visualisation", "visualisation.kv"))
)
