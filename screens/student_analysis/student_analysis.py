from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
import utils, os


class StudentAnalysis(MDScreen):
    pass


Builder.load_file(
    utils.get_path(os.path.join("screens", "student_analysis", "student_analysis.kv"))
)
