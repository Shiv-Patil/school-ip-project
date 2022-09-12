from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import (
    ColorProperty,
    BooleanProperty,
    ObjectProperty,
    NumericProperty,
)
from kivymd.app import MDApp
from kivy.animation import Animation

app = None

kv = """
<Dialog>:
    size_hint: None, None
    size: 0, 0
    MDAnchorLayout:
        id: anchor
        md_bg_color: root.overlay_color[:3] + [root.overlay_color[-1] * root._anim_alpha]
        size_hint: None, None
        size: root.parent.size if root.parent else Window.size
"""
Builder.load_string(kv)


class Dialog(FloatLayout):
    auto_dismiss = BooleanProperty(False)
    overlay_color = ColorProperty((0, 0, 0, 0.4))
    _is_open = BooleanProperty(False)
    content_cls = ObjectProperty()
    _anim_alpha = NumericProperty(0)
    _anim_duration = NumericProperty(0.1)
    __events__ = ("on_open", "on_dismiss")

    def __init__(self, **kwargs):
        super(Dialog, self).__init__(**kwargs)
        global app
        app = MDApp.get_running_app()

    def on_kv_post(self, base_widget):
        if self.content_cls:
            self.ids.anchor.add_widget(self.content_cls)

    def on_touch_down(self, touch):
        if self.ids.anchor.collide_point(*touch.pos):
            if self.content_cls:
                if not self.content_cls.collide_point(*touch.pos):
                    if self.auto_dismiss:
                        self.dismiss()
                else:
                    self.content_cls.on_touch_down(touch)
            return True

    def open(self, *_args, **kwargs):
        if self._is_open:
            return app.logger.warning("App: Dialog already open")

        app.root.add_widget(self)
        self._is_open = True
        Window.bind(on_key_up=self._handle_keyboard)

        if kwargs.get("animation", True):
            ani = Animation(_anim_alpha=1.0, d=self._anim_duration)
            ani.bind(on_complete=lambda *_args: self.dispatch("on_open"))
            ani.start(self)
        else:
            self._anim_alpha = 1.0
            self.dispatch("on_open")

    def dismiss(self, *_args, **kwargs):
        if not self._is_open:
            return app.logger.warning("App: Dialog already closed")

        if kwargs.get("animation", True):
            ani = Animation(
                _anim_alpha=0.0,
                d=self._anim_duration / 4,
            )
            ani.bind(on_complete=lambda *_args: self._real_remove_widget())
            ani.start(self)
        else:
            self._anim_alpha = 0
            self._real_remove_widget()

    def _real_remove_widget(self):
        if not self._is_open:
            return

        app.root.remove_widget(self)
        Window.unbind(on_key_up=self._handle_keyboard)
        self._is_open = False
        self.dispatch("on_dismiss")

    def on_open(self):
        pass

    def on_dismiss(self):
        pass

    def _handle_keyboard(self, instance, key, *args):
        if (
            key in (1001, 27)
            and self.auto_dismiss
            and self._is_open
            and not app.loading
        ):
            self.dismiss()
            return True
