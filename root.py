from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon
from kivy.uix.screenmanager import CardTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import HoverBehavior
import importlib
from kivymd.material_resources import DEVICE_TYPE

app = MDApp.get_running_app()
kv = """
#:import Window kivy.core.window.Window
#:import get_path utils.get_path
#:import os os
<TitleBtn>
    icon: "circle"
    pos_hint: {"center_x": .5, "center_y": .5}
    font_size: dp(20)
    color: [0, 0.8, 0.14, 1]
    draggable: False
    on_enter:
        Window.set_system_cursor('hand')
    on_leave:
        Window.set_system_cursor('arrow')
<LoadingOverlay>
    size_hint: None, None
    size: 0, 0
    MDAnchorLayout:
        id: anchor
        md_bg_color: (0, 0, 0, .1)
        size_hint: None, None
        width: Window.width
        Image:
            source: get_path(os.path.join("assets", "loading.gif"))
            anim_loop: -1
            anim_delay: 0.03
            size_hint: None, None
            size: dp(256), dp(256)
<Root>:
    orientation: "vertical"
    MDBoxLayout:
        id: title_bar
        md_bg_color: app.theme_cls.bg_dark
        orientation: "horizontal"
        size_hint_y: None
        height: dp(69/2)
        Widget:
        MDLabel:
            text: "Student Analysis"
            font_style: "Subtitle2"
            halign: "center"
        MDAnchorLayout:
            anchor_x: "right"
            MDGridLayout:
                cols: 3
                spacing: dp(5)
                size_hint_x: None
                width: dp(80)
                adaptive_height: True
                TitleBtn:
                    color: [0, 0.8, 0.14, 1]
                    on_release:
                        Window.minimize()
                TitleBtn:
                    color: [1, 0.75, 0, 1]
                    on_release:
                        Window.maximize()
                TitleBtn:
                    color: [1, 0.37, 0.3, 1]
                    on_release:
                        app.stop()
"""
Builder.load_string(kv)


class Root(MDBoxLayout):

    history = ListProperty()
    SCREENS = {
        "dashboard": "Dashboard",
        "display": "Display",
        "edit": "Edit",
        "student_analysis": "StudentAnalysis",
        "class_analysis": "ClassAnalysis",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager = MDScreenManager()
        self.add_widget(self.manager)
        self.manager.transition = CardTransition()
        Window.bind(on_key_up=self._handle_keyboard)

        self.loading_widget = LoadingOverlay()

        if self._set_custom_titlebar():
            titlebar_height = self.ids.title_bar.height
            Window.bind(
                height=lambda obj, val: self.loading_widget.ids.anchor.setter("height")(
                    obj, val - titlebar_height
                )
            )

    def show_loading(self):
        self.add_widget(self.loading_widget)

    def hide_loading(self):
        self.remove_widget(self.loading_widget)

    def goto(self, screen_name, side="left", _from_goback=False):
        if screen_name not in self.SCREENS:
            app.logger.error("APP", "Screen not found: " + screen_name)
            return

        if not self.manager.has_screen(screen_name):
            screen_object = getattr(
                importlib.import_module(f"screens.{screen_name}.{screen_name}"),
                self.SCREENS.get(screen_name),
            )()
            screen_object.name = screen_name
            self.manager.add_widget(screen_object)

        if not _from_goback:
            self.history.append({"name": screen_name, "side": side})

        self.manager.transition.direction = side
        self.manager.current = screen_name

    def _handle_keyboard(self, instance, key, *args):
        if key in (1001, 27):
            self.goback()
            return True

    def goback(self):
        if len(self.history) > 1:
            prev_side = self.history.pop()["side"]
            prev_screen = self.history[-1]
            side = "left" if prev_side == "right" else "right"

            self.goto(prev_screen["name"], side=side, _from_goback=True)

    def _set_custom_titlebar(self):
        wid = self.ids.title_bar
        if DEVICE_TYPE == "desktop":
            if not Window.custom_titlebar:
                Window.custom_titlebar = True
                if Window.set_custom_titlebar(wid):
                    return True
            else:
                app.Logger.warning("APP", "Window: titlebar already added")
                return True

        self.remove_widget(wid)
        app.Logger.error("APP", "Window: setting custom titlebar not allowed")
        return False


class TitleBtn(ButtonBehavior, MDIcon, HoverBehavior):
    pass


class LoadingOverlay(FloatLayout):
    def on_touch_down(self, touch):
        if self.ids.anchor.collide_point(*touch.pos):
            return True
