from kivy.app import App
 
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
 
from kivy.core.text import LabelBase, DEFAULT_FONT 
LabelBase.register(DEFAULT_FONT, "ipaexg.ttf") 
 
Window.size = (400,400)
 
class MyWidget(BoxLayout):
    pass
 
class My0App(App):
    def build(self):
        mywidget = MyWidget()
        return mywidget
 
My0App().run()