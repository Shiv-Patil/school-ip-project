import os, sys, json
from kivy.config import Config
from kivy.resources import resource_add_path
import widgets

Config.set("kivy", "exit_on_escape", "0")
Config.set("graphics", "minimum_width", "530")
Config.set("graphics", "minimum_height", "310")


def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    return os.path.join(base_path, relative_path)


resource_add_path(get_path(os.path.join("screens", "dashboard")))
resource_add_path(get_path(os.path.join("screens", "display")))
resource_add_path(get_path(os.path.join("screens", "edit")))
resource_add_path(get_path(os.path.join("screens", "student_analysis")))
resource_add_path(get_path(os.path.join("screens", "class_analysis")))

with open(get_path("colors.json")) as f:
    colors = json.load(f)
