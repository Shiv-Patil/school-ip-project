from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import utils, os
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.effects.scroll import ScrollEffect

app = MDApp.get_running_app()


class Display(MDScreen):
    data_table = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_enter(self, *args):
        if not self.data_table:
            self._create_table()
        return super().on_enter(*args)

    def _create_table(self):
        self.data_table = MDDataTable(
            size_hint_max_x=1074,
            elevation=1,
            rows_num=20,
            background_color_selected_cell=app.theme_cls.bg_normal,
            effect_cls=ScrollEffect,
            column_data=[
                ("Id", dp(15)),
                ("First Name", dp(40)),
                ("Middle Name", dp(40)),
                ("Last Name", dp(40)),
                ("Class", dp(20)),
                ("Division", dp(20)),
                ("Academic year", dp(30)),
            ],
        )
        self.data_table.ids.container.children[0].bar_width = 4
        self.data_table.ids.container.children[0].smooth_scroll_end = 10
        self.data_table.ids.container.children[0].scroll_type = ["bars", "content"]
        for child in self.data_table.ids.container.children[1].ids.header.children:
            child.tooltip_text = ""
        self.data_table.ids.container.children[1].ids.first_cell.tooltip_text = ""
        self.ids.datatable_wrapper.add_widget(self.data_table)


Builder.load_file(utils.get_path(os.path.join("screens", "display", "display.kv")))
