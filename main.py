import utils, importlib
from kivymd.app import MDApp
from kivy.logger import Logger
from threading import Thread
from kivy.clock import mainthread
import logging

logging.getLogger("PIL").setLevel(logging.ERROR)


class StudentAnalysis(MDApp):

    name = "student analysis"
    title = "student analysis"
    logger = Logger
    loading = False

    def build(self):
        self.theme_cls.colors = utils.colors
        self.theme_cls.primary_palette = "Teal"
        self.root = importlib.import_module("root").Root()
        self.database = importlib.import_module("sqloperator").SqlOperator()

    def on_start(self):
        self.root.goto("dashboard")

    def start_task(
        self, func, after=None, start_loading_func=True, stop_loading_func=True
    ):
        if start_loading_func is True or stop_loading_func is True:
            start_loading_func = self.root.show_loading
            stop_loading_func = self.root.hide_loading

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


if __name__ == "__main__":
    StudentAnalysis().run()
