import utils, importlib
from kivymd.app import MDApp
from kivy.logger import Logger
from threading import Thread
from kivy.clock import mainthread
from widgets.toast import Toast
import logging

logging.getLogger("PIL").setLevel(logging.ERROR)
logging.getLogger("matplotlib").setLevel(logging.ERROR)


class StudentAnalysis(MDApp):

    name = "student analysis"
    title = "student analysis"
    logger = Logger
    loading = False
    _toast = None

    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Light"
        self.theme_cls.colors = utils.colors
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.material_style = "M3"
        self.root = importlib.import_module("root").Root()
        self.database = importlib.import_module("sqloperator").SqlOperator()
        self._toast = Toast()

    def open_settings(self, *args):
        pass

    def switch_theme(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )

    def on_start(self):
        self.root.goto("dashboard")

    def start_task(
        self,
        func,
        after=None,
        use_overlay=True,
        show_loading_anim=True,
        overlay_color=(0, 0, 0, 0.4),
    ):
        start_loading_func, stop_loading_func = (
            (
                lambda: self.root.show_loading(show_loading_anim, overlay_color),
                self.root.hide_loading,
            )
            if use_overlay
            else (lambda: 0, lambda: 0)
        )

        @mainthread
        def callback(result):
            stop_loading_func()
            self.loading = False
            if callable(after):
                after(result)

        def task():
            callback(func())

        self.loading = True
        start_loading_func()
        thread = Thread(target=task)
        thread.daemon = True
        thread.start()

    @mainthread
    def toast(self, msg):
        self._toast.toast(msg)


if __name__ == "__main__":
    StudentAnalysis().run()
