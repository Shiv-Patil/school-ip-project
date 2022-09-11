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

    def start_task(self, func, after=None):
        @mainthread
        def callback(result):
            self.root.hide_loading()
            self.loading = False
            if callable(after):
                after(result)

        def task():
            callback(func())

        self.loading = True
        self.root.show_loading()
        thread = Thread(target=task)
        thread.daemon = True
        thread.start()


if __name__ == "__main__":
    StudentAnalysis().run()
