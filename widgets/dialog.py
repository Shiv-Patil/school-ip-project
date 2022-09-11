from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import ColorProperty, BooleanProperty, ObjectProperty
from kivymd.app import MDApp

app = None

kv = """
<Dialog>:
    size_hint: None, None
    size: 0, 0
    MDAnchorLayout:
        id: anchor
        md_bg_color: root.overlay_color
        size_hint: None, None
        size: root.parent.size if root.parent else Window.size
"""
Builder.load_string(kv)


class Dialog(FloatLayout):
    auto_dismiss = BooleanProperty(False)
    overlay_color = ColorProperty((0, 0, 0, 0.5))
    _is_open = BooleanProperty(False)
    content_cls = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        global app
        app = MDApp.get_running_app()

    def on_kv_post(self, base_widget):
        if self.content_cls:
            self.ids.anchor.add_widget(self.content_cls)

    def on_touch_down(self, touch):
        if self.ids.anchor.collide_point(*touch.pos):
            return True

    def open(self):
        if not self._is_open:
            app.root.add_widget(self)
            self._is_open = True
        else:
            app.logger.warning("App: Dialog already open")

    def dismiss(self):
        if self._is_open:
            app.root.remove_widget(self)
            self._is_open = False
        else:
            app.logger.warning("App: Dialog already closed")
