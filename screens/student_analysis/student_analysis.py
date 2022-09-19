from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import utils, os
from kivy.properties import StringProperty
from kivymd.uix.menu import MDDropdownMenu
from kivy.effects.scroll import ScrollEffect
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.app import MDApp

app = MDApp.get_running_app()


class StudentAnalysis(MDScreen):
    _student_id = StringProperty("")
    _fullname = StringProperty("")
    yearmenu = None

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

        self.ids.year.set_item(str(years[0][5]))

        def set_item(text_item):
            Clock.schedule_once(lambda dt: self.yearmenu.dismiss(), 0.169)
            Clock.schedule_once(lambda dt: self.ids.year.set_item(text_item), 0.1)

        menu_items = []
        for year in years:
            menu_items.append(
                {
                    "viewclass": "OneLineListItem",
                    "text": str(year[5]),
                    "height": dp(52),
                    "on_release": lambda x=str(year[5]): set_item(x),
                }
            )

        self.yearmenu.items = menu_items

    def _create_dropdown(self):
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


Builder.load_file(
    utils.get_path(os.path.join("screens", "student_analysis", "student_analysis.kv"))
)
