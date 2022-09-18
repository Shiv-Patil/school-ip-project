from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDIcon
from kivy.uix.screenmanager import CardTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import HoverBehavior, CommonElevationBehavior
import importlib
from kivymd.material_resources import DEVICE_TYPE
from widgets.dialog import Dialog
from kivy.clock import Clock

app = MDApp.get_running_app()
kv = """
#:import Window kivy.core.window.Window
#:import get_path utils.get_path
#:import os os

<TitleBtn, ElevationTitleBtn>:
    icon: "circle"
    pos_hint: {"center_x": .5, "center_y": .5}
    font_size: dp(20)
    size_hint: None, None
    size: self.texture_size
    elevation: 1
    color: "black"
    draggable: False
    on_enter:
        Window.set_system_cursor('hand') if self.do_hover else 0
    on_leave:
        Window.set_system_cursor('arrow')

<LoadingImage>:
    source: get_path(os.path.join("assets", "loading.gif"))
    anim_loop: -1
    anim_delay: 0.03
    size_hint: None, None
    size: dp(256), dp(256)

<TitleBar>:
    md_bg_color: app.theme_cls.bg_dark
    orientation: "horizontal"
    size_hint_y: None
    height: dp(69/2)
    pos_hint: {"top":1}
    MDAnchorLayout:
        anchor_x: "left"
        padding: dp(7), 0
        TitleBtn:
            id: back_btn
            icon: "menu-left"
            font_size: "24dp"
            detect_visible: False
            on_release: app.root.goback()
    MDLabel:
        text: "Student Analysis"
        font_style: "Subtitle2"
        halign: "center"
    MDAnchorLayout:
        anchor_x: "right"
        MDGridLayout:
            cols: 3
            spacing: dp(5)
            adaptive_size: True
            width: dp(80)
            padding: dp(7), 0
            ElevationTitleBtn:
                color: [0, 0.8, 0.14, 1]
                on_release: Window.minimize()
            ElevationTitleBtn:
                color: [1, 0.75, 0, 1]
                on_release: Window.maximize()
            ElevationTitleBtn:
                color: [1, 0.37, 0.3, 1]
                on_release: app.stop()

<Root>:
    orientation: "vertical"
    size_hint_y: None
    height: Window.height - dp(69/2)
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

        self.title_bar = TitleBar()
        Window.add_widget(self.title_bar)

        self.manager = MDScreenManager()
        self.add_widget(self.manager)
        self.manager.transition = CardTransition()

        Window.bind(on_key_up=self._handle_keyboard)
        self.bind(history=self.on_history_change)

        self.loading_widget = Dialog(content_cls=LoadingImage())

        self._set_custom_titlebar()

    def show_loading(self, anim=True, overlay_color=(0, 0, 0, 0.4)):
        self.loading_widget.content_cls.opacity = 0 if not anim else 1
        self.loading_widget.overlay_color = overlay_color
        self.loading_widget.open()

    def hide_loading(self):
        self.loading_widget.dismiss()

    def goto(self, screen_name, side="left", _from_goback=False):
        if screen_name not in self.SCREENS:
            app.logger.error("APP: Screen not found: " + screen_name)
            return

        if screen_name == self.manager.current:
            app.logger.warning("APP: Cannot switch to same screen: " + screen_name)
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

        def _change_screen(self):
            self.manager.current = screen_name

        Clock.schedule_once(lambda dt: _change_screen(self))

    def _handle_keyboard(self, instance, key, *args):
        if key in (1001, 27):
            if not app.loading:
                self.goback()
            return True

    def goback(self):
        if len(self.history) > 1:
            prev_side = self.history.pop()["side"]
            prev_screen = self.history[-1]
            side = "left" if prev_side == "right" else "right"

            self.goto(prev_screen["name"], side=side, _from_goback=True)

    def on_history_change(self, inst, history):
        back_btn = self.title_bar.ids.back_btn
        if len(history) > 1:
            back_btn.opacity = "1"
            back_btn.do_hover = True
        else:
            back_btn.opacity = "0"
            back_btn.do_hover = False
            Window.set_system_cursor("arrow")

    def _set_custom_titlebar(self):
        wid = self.title_bar
        if DEVICE_TYPE == "desktop":
            if not Window.custom_titlebar:
                Window.custom_titlebar = True
                if Window.set_custom_titlebar(wid):
                    return True
            else:
                app.logger.warning("App: Window: titlebar already added")
                return True

        Window.custom_titlebar = False
        Window.remove_widget(wid)
        self.size_hint_y = 1
        app.logger.error("App: Window: setting custom titlebar not allowed")
        return False


class TitleBar(MDBoxLayout):
    pass


class TitleBtn(ButtonBehavior, MDIcon, HoverBehavior):
    do_hover = BooleanProperty(False)


class ElevationTitleBtn(CommonElevationBehavior, TitleBtn):
    do_hover = BooleanProperty(True)


class LoadingImage(Image):
    pass
