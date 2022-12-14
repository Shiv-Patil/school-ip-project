"""
Register KivyMD widgets to use without import.
"""

from kivy.factory import Factory

register = Factory.register
register("MDScrollView", module="kivymd.uix.scrollview")
register("MDRecycleView", module="kivymd.uix.recycleview")
register("MDResponsiveLayout", module="kivymd.uix.responsivelayout")
register("MDSegmentedControl", module="kivymd.uix.segmentedcontrol")
register("MDSegmentedControlItem", module="kivymd.uix.segmentedcontrol")
register("MDWidget", module="kivymd.uix.widget")
register("MDFloatLayout", module="kivymd.uix.floatlayout")
register("MDAnchorLayout", module="kivymd.uix.anchorlayout")
register("MDRecycleGridLayout", module="kivymd.uix.recyclegridlayout")
register("MDBoxLayout", module="kivymd.uix.boxlayout")
register("MDRelativeLayout", module="kivymd.uix.relativelayout")
register("MDGridLayout", module="kivymd.uix.gridlayout")
register("MDStackLayout", module="kivymd.uix.stacklayout")
register("FitImage", module="kivymd.uix.fitimage")
register("MDTooltip", module="kivymd.uix.tooltip")
register("MDIconButton", module="kivymd.uix.button")
register("MDFlatButton", module="kivymd.uix.button")
register("MDRaisedButton", module="kivymd.uix.button")
register("MDFloatingActionButton", module="kivymd.uix.button")
register("MDRectangleFlatButton", module="kivymd.uix.button")
register("MDTextButton", module="kivymd.uix.button")
register("MDCustomRoundIconButton", module="kivymd.uix.button")
register("MDRoundFlatButton", module="kivymd.uix.button")
register("MDFillRoundFlatButton", module="kivymd.uix.button")
register("MDRectangleFlatIconButton", module="kivymd.uix.button")
register("MDRoundFlatIconButton", module="kivymd.uix.button")
register("MDFillRoundFlatIconButton", module="kivymd.uix.button")
register("MDCard", module="kivymd.uix.card")
register("MDSeparator", module="kivymd.uix.card")
register("MDLabel", module="kivymd.uix.label")
register("MDIcon", module="kivymd.uix.label")
register("MDList", module="kivymd.uix.list")
register("ILeftBody", module="kivymd.uix.list")
register("ILeftBodyTouch", module="kivymd.uix.list")
register("IRightBody", module="kivymd.uix.list")
register("IRightBodyTouch", module="kivymd.uix.list")
register("OneLineListItem", module="kivymd.uix.list")
register("TwoLineListItem", module="kivymd.uix.list")
register("ThreeLineListItem", module="kivymd.uix.list")
register("OneLineAvatarListItem", module="kivymd.uix.list")
register("TwoLineAvatarListItem", module="kivymd.uix.list")
register("ThreeLineAvatarListItem", module="kivymd.uix.list")
register("OneLineIconListItem", module="kivymd.uix.list")
register("TwoLineIconListItem", module="kivymd.uix.list")
register("ThreeLineIconListItem", module="kivymd.uix.list")
register("OneLineRightIconListItem", module="kivymd.uix.list")
register("TwoLineRightIconListItem", module="kivymd.uix.list")
register("ThreeLineRightIconListItem", module="kivymd.uix.list")
register("OneLineAvatarIconListItem", module="kivymd.uix.list")
register("TwoLineAvatarIconListItem", module="kivymd.uix.list")
register("ThreeLineAvatarIconListItem", module="kivymd.uix.list")
register("HoverBehavior", module="kivymd.uix.behaviors.hover_behavior")
register("FocusBehavior", module="kivymd.uix.behaviors.focus_behavior")
register("MagicBehavior", module="kivymd.uix.behaviors.magic_behavior")
register("MDProgressBar", module="kivymd.uix.progressbar")
register("MDScrollViewRefreshLayout", module="kivymd.uix.refreshlayout")
register("MDTextField", module="kivymd.uix.textfield")
register("MDTextFieldRect", module="kivymd.uix.textfield")
register("MDDropDownItem", module="kivymd.uix.dropdownitem")
