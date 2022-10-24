from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDIcon
from kivy.uix.screenmanager import SlideTransition as ScreenTransition
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import HoverBehavior
import importlib
import platform
from widgets.dialog import Dialog
from kivy.clock import Clock

app = MDApp.get_running_app()
kv = """
#:import Window kivy.core.window.Window
#:import get_path utils.get_path
#:import os os
#:import ScrollEffect kivy.effects.scroll.ScrollEffect

<TitleBtn>:
    icon: "circle"
    pos_hint: {"center_x": .5, "center_y": .5}
    font_size: dp(20)
    size_hint: None, None
    size: self.texture_size
    elevation: 1
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
    md_bg_color: "#DDE0E8" if app.theme_cls.theme_style == "Light" else "#1F1F1F"
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
        text: root.title_text
        font_style: "Subtitle2"
        halign: "center"
    MDAnchorLayout:
        anchor_x: "right"
        MDGridLayout:
            id: title_btn_container
            rows: 1
            spacing: dp(5)
            adaptive_size: True
            width: dp(80)
            padding: dp(7), 0
            TitleBtn:
                icon: "theme-light-dark"
                on_release: app.switch_theme()

<TitleControlButtons>:
    adaptive_size: True
    spacing: dp(5)
    rows: 1
    TitleBtn:
        icon: "window-minimize"
        on_release: Window.minimize()
    TitleBtn:
        icon: "window-close"
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
        "analysis": "Analysis",
        "visualisation": "Visualisation",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.title_bar = TitleBar()
        Window.add_widget(self.title_bar)

        self._set_custom_titlebar()

        self.manager = ScreenManager()
        self.add_widget(self.manager)
        self.transition = ScreenTransition()

        Window.bind(on_key_up=self._handle_keyboard)
        self.bind(history=self.on_history_change)

        self.loading_widget = Dialog(content_cls=LoadingImage())
        self.loading_widget.bind(on_open=self.on_loading_open)

    def on_loading_open(self):
        pass

    def show_loading(
        self, anim=True, overlay_color=(0, 0, 0, 0.4), onopen=lambda *args: 0
    ):
        self.loading_widget.content_cls.opacity = 0 if not anim else 1
        self.loading_widget.overlay_color = overlay_color
        self.on_loading_open = onopen
        self.loading_widget.open()

    def hide_loading(self):
        self.loading_widget.dismiss()

    def goto(
        self,
        screen_name,
        side="left",
        _from_goback=False,
        transition=None,
        callback=lambda: 0,
    ):
        if screen_name not in self.SCREENS:
            app.logger.error("APP: Screen not found: " + screen_name)
            return

        if screen_name == self.manager.current:
            app.logger.warning("APP: Cannot switch to same screen: " + screen_name)
            return

        self.manager.transition = self.transition if not transition else transition

        if not self.manager.has_screen(screen_name):
            self.show_loading()
            screen_object = getattr(
                importlib.import_module(f"screens.{screen_name}.{screen_name}"),
                self.SCREENS.get(screen_name),
            )()
            screen_object.name = screen_name
            self.manager.add_widget(screen_object)
            self.hide_loading()

        if not _from_goback:
            self.history.append({"name": screen_name, "side": side})

        self.manager.transition.direction = side

        def _change_screen(self):
            scrn = self.manager.get_screen(screen_name)
            if hasattr(scrn, "before_enter"):
                scrn.before_enter()

            def _set_scrn():
                self.manager.current = screen_name
                callback()
                self.title_bar.title_text = screen_name

            Clock.schedule_once(lambda dt: _set_scrn(), 0.1)

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
        if platform.system() == "Linux":
            if Window.set_custom_titlebar(wid):
                self.title_bar.ids.title_btn_container.add_widget(TitleControlButtons())
                return True

        Window.custom_titlebar = False
        return False


class TitleBar(MDBoxLayout):
    title_text = StringProperty("")


class TitleBtn(ButtonBehavior, MDIcon, HoverBehavior):
    do_hover = BooleanProperty(True)


class TitleControlButtons(MDGridLayout):
    pass


class LoadingImage(Image):
    pass
