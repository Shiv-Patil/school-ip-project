from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ColorProperty, NumericProperty, ListProperty
from kivy.uix.label import Label
from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout

Builder.load_string(
    """
<Toast>:
    size_hint: None, None
    size: 0, 0
    MDAnchorLayout:
        md_bg_color: 0, 0, 0, 0
        size_hint: None, None
        size: Window.size
        anchor_y: "bottom"
        padding: dp(40)

        MDCard:
            id: box
            size_hint: None, None
            size: self.minimum_size
            padding: dp(10)
            elevation: 2.3
            opacity: 0
            canvas:
                Color:
                    rgba: root._md_bg_color
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: root.radius
"""
)


class Toast(FloatLayout):
    duration = NumericProperty(2.5)
    _md_bg_color = ColorProperty([0.95, 0.95, 0.95, 1])
    radius = ListProperty([dp(7), dp(7), dp(7), dp(7)])
    _is_open = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global app
        app = MDApp.get_running_app()

    def on_kv_post(self, *args):
        self.label_toast = Label(size_hint=(None, None), opacity=0)
        self.label_toast.color = "black"
        self.ids.box.add_widget(self.label_toast)

    def toast(self, text_toast: str) -> None:

        if self._is_open:
            return
        self.label_toast.text = text_toast
        self.label_toast.texture_update()
        self.label_toast.size = self.label_toast.texture_size
        self._is_open = True
        app.root.add_widget(self)
        self.on_open()

    def dismiss(self):
        app.root.remove_widget(self)
        self._is_open = False

    def on_open(self) -> None:

        self.fade_in()
        Clock.schedule_once(self.fade_out, self.duration)

    def fade_in(self) -> None:

        anim = Animation(opacity=1, duration=0.4)
        anim.start(self.label_toast)
        anim.start(self.ids.box)

    def fade_out(self, *args) -> None:

        anim = Animation(opacity=0, duration=0.4)
        anim.bind(on_complete=lambda *x: self.dismiss())
        anim.start(self.label_toast)
        anim.start(self.ids.box)

    def on_touch_down(self, touch):
        return super().on_touch_down(touch)
