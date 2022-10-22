from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import utils, os
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.effects.scroll import ScrollEffect
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from functools import partial
from . import search_data, delete_data, edit_data

app = MDApp.get_running_app()


class Display(Screen):
    data_table = None
    menu = None
    delete_dialog = None
    edit_dialog = None

    def before_enter(self):
        if not self.data_table:
            self._create_table()
        if not self.menu:
            self._create_dropdown()
        delete_data.init_deletemodal(self)
        edit_data.init_editmodal(self)

    def on_leave(self, *_args):
        self.data_table.ids.container.children[0].scroll_x = 0
        self.data_table.ids.container.children[0].scroll_y = 0
        self.data_table.update_row_data(self.data_table, {})

    def _on_edit_button_pressed(self):
        self.edit_dialog.open()

    def _on_delete_button_pressed(self):
        self.delete_dialog.open()

    def _on_show_button_pressed(self):
        self.populate_rows()

    def populate_rows(self):
        _num_results = int(self.ids.num_results.current_item.split()[0])
        _std = self.ids.class_field.text.strip()
        _id_name = self.ids.id_name_field.text.strip()

        if len(_id_name) == 0:
            _id_name = "%"

        def callback(rows):
            if not isinstance(rows, list):
                return
            self.data_table.update_row_data(self.data_table, rows)

        app.start_task(
            partial(search_data.get_rows, _num_results, _std, _id_name, app), callback
        )

    def _create_dropdown(self):
        def set_item(text_item):
            Clock.schedule_once(lambda dt: self.menu.dismiss(), 0.169)
            Clock.schedule_once(
                lambda dt: self.ids.num_results.set_item(text_item), 0.1
            )

        self.ids.num_results.set_item("05 Rows")
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": f"{i} Rows",
                "height": dp(52),
                "on_release": lambda x=f"{i} Rows": set_item(x),
            }
            for i in ("05", "10", "15", "20", "50", "100")
        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.num_results,
            items=menu_items,
            position="bottom",
            width_mult=2,
            background_color="white",
            opening_time=0,
            elevation=1,
        )
        self.menu.ids.md_menu.effect_cls = ScrollEffect
        self.menu.ids.md_menu.children[0].padding = (0, 0, 0, 0)

    def _create_table(self):
        self.data_table = MDDataTable(
            size_hint_max_x=1074,
            elevation=1,
            rows_num=100,
            effect_cls=ScrollEffect,
            column_data=[
                ("Id", dp(15), lambda d: int(d)),
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
