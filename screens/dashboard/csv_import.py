from pandas_schema import Column, Schema
from pandas_schema.validation import InRangeValidation
from kivy.core.window import Window
import pandas
import numpy
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from widgets.dialog import Dialog
from kivy.lang import Builder
from kivy.properties import ColorProperty, StringProperty, BooleanProperty
from plyer import filechooser
from kivy.clock import mainthread
import utils
import os

app = MDApp.get_running_app()


class ImportModalContainer(MDCard):
    upload_icon_color = ColorProperty([0.78, 0.78, 0.78, 1])
    filepath = StringProperty("")
    _choosing_file = BooleanProperty(False)

    def on_kv_post(self, _):
        Window.bind(on_drop_file=self._file_dropped)

    def dialog_dismissed(self, _inst):
        self.upload_icon_color = [0.78, 0.78, 0.78, 1]
        self.filepath = ""

    def _file_dropped(self, _inst, file: bytes, *_args):
        self._file_selected(file.decode())

    def _on_browse_button_clicked(self):
        def _after(result):
            self._choosing_file = False

        self._choosing_file = True
        app.start_task(
            lambda *args: filechooser.open_file(
                on_selection=lambda f: self._file_selected(f[0])
            ),
            _after,
            show_loading_anim=False,
            overlay_color=(0, 0, 0, 0.1),
        )

    @mainthread
    def _file_selected(self, filepath: str):
        if filepath.endswith(".csv"):
            self.filepath = filepath
            self.upload_icon_color = [0.34, 0.68, 0.91, 1]
        else:
            app.toast("Please select a valid csv file")


Builder.load_file(utils.get_path(os.path.join("screens", "dashboard", "csv_import.kv")))
schema = Schema(
    [
        Column("id"),
        Column("f_name"),
        Column("m_name", allow_empty=True),
        Column("l_name", allow_empty=True),
        Column("std", [InRangeValidation(1, 13)]),
        Column("div", allow_empty=True),
        Column("roll_no"),
        Column("year"),
        Column("unit1-math", allow_empty=True),
        Column("unit1-eng", allow_empty=True),
        Column("unit1-phy", allow_empty=True),
        Column("unit1-chem", allow_empty=True),
        Column("unit1-ip", allow_empty=True),
        Column("term1-math", allow_empty=True),
        Column("term1-eng", allow_empty=True),
        Column("term1-phy", allow_empty=True),
        Column("term1-chem", allow_empty=True),
        Column("term1-ip", allow_empty=True),
        Column("unit2-math", allow_empty=True),
        Column("unit2-eng", allow_empty=True),
        Column("unit2-phy", allow_empty=True),
        Column("unit2-chem", allow_empty=True),
        Column("unit2-ip", allow_empty=True),
        Column("term2-math", allow_empty=True),
        Column("term2-eng", allow_empty=True),
        Column("term2-phy", allow_empty=True),
        Column("term2-chem", allow_empty=True),
        Column("term2-ip", allow_empty=True),
    ]
)


def init_importmodal(self):
    if not self.dialog:
        self.import_csv_container = ImportModalContainer()
        self.dialog = Dialog(
            auto_dismiss=True,
            content_cls=self.import_csv_container,
            overlay_color=(0, 0, 0, 0.6),
        )
        self.dialog.bind(on_dismiss=self.import_csv_container.dialog_dismissed)


def _read_csv_and_validate(filepath):
    df = pandas.read_csv(filepath)
    validated = schema.validate(df)
    if len(validated) == 0:
        return df
    else:
        for error in validated:
            app.logger.error("CSV validator: " + str(error))
        return False


def import_csv_in_database(csv, set_progress):
    df = _read_csv_and_validate(csv)
    if df is False:
        return False
    df.drop_duplicates(inplace=True)
    total_rows = len(df)
    rows_added = 0
    unique_added = numpy.array([])
    for _, data in df.iterrows():
        id = data.at["id"]
        if not numpy.isin(id, unique_added):
            unique_added = numpy.append(unique_added, id)
            app.database.execute_query(
                "INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?)",
                data.loc[:"l_name"],
            )
        app.database.execute_query(
            "INSERT INTO academic_year (student, class, division, rollno, year_start) VALUES (?, ?, ?, ?, ?)",
            data.loc[["id", "std", "div", "roll_no", "year"]],
        )
        academic_year_id = app.database.execute_query(
            "SELECT id from academic_year WHERE student=? AND year_start=?",
            (id, data.at["year"]),
        )[0][0]
        for exam in ["unit1", "unit2", "term1", "term2"]:
            app.database.execute_query(
                "INSERT INTO marks (academic_year, exam, mathematics, english, phyiscs, chemistry, informatics_practices) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (academic_year_id,)
                + (exam,)
                + tuple(data.loc[f"{exam}-math":f"{exam}-ip"]),
            )
        rows_added += 1
        set_progress(round((rows_added / total_rows) * 100))
    return True
