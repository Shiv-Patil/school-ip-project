import platform, os, sys, json, platform
from kivy.config import Config

if platform.system() == "Windows":
    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"


def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(sys.argv[0]))

    return os.path.join(base_path, relative_path)


Config.read(get_path("config.ini"))
from kivy.resources import resource_add_path
import widgets

resource_add_path(get_path(os.path.join("screens", "dashboard")))
resource_add_path(get_path(os.path.join("screens", "display")))
resource_add_path(get_path(os.path.join("screens", "edit")))
resource_add_path(get_path(os.path.join("screens", "student_analysis")))
resource_add_path(get_path(os.path.join("screens", "class_analysis")))

with open(get_path("colors.json")) as f:
    colors = json.load(f)

grades = {90: "A1", 80: "A2", 70: "B1", 60: "B2", 50: "C1", 40: "C2", 32: "D", 0: "E"}

pie_colors = dict(
    zip(
        grades.values(),
        (
            "#007F4E",
            "#003F5C",
            "#43B0F1",
            "#FF6B45",
            "#FFAB05",
            "#58508D",
            "#D52DB7",
            "#E12729",
        ),
    )
)


def get_grade(p):
    for threshold, grade in grades.items():
        if p > threshold:
            return grade
    return "Not graded"
