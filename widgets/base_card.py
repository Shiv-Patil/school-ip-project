from kivy.factory import Factory
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import CommonElevationBehavior

kv = """
<BaseCard>:
    elevation: 2.4
    shadow_softness: 16
    radius: 8
    md_bg_color: app.theme_cls.bg_light
"""
Builder.load_string(kv)


class BaseCard(CommonElevationBehavior, MDBoxLayout):
    pass


Factory.register("BaseCard", BaseCard)
