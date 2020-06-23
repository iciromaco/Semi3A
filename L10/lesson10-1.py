from kivy.app import App
from kivy.lang import Builder
 
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
 
from kivy.core.text import LabelBase, DEFAULT_FONT 
LabelBase.register(DEFAULT_FONT, "ipaexg.ttf") 
 
Builder.load_string('''
#: set dummy './prof.jpg'
<MyWidget>
    orientation: 'vertical'
    Image:
        id: pic0
        allow_stretch: True
        source : dummy
    Button:
        id: but0
        # text: 'ボタン'
        font_size: 36
        font_name: 'ipaexg.ttf'
''')
 
Window.size = (400,400)
 
class MyWidget(BoxLayout):
    pass
 
class MyApp(App):
    def build(self):
        mywidget = MyWidget()
        mywidget.ids['but0'].text = 'ボタン'
        return mywidget
 
MyApp().run()