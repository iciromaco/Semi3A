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
    Label:
        size_hint_y: None
        height: 32
        id: label0
        # text : '入力画像'
        font_size: 20
    Image:
        size_hint_y: 7
        id: pic0
        allow_stretch: True
        source : dummy
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: 32
        Spinner:
            size_hint_x: None
            width:100
            id: sp0
            text: 'Menu'
            on_press: root.do_menu()
        TextInput:
            id: path0
            text: './prof.jpg'
            multiline: False
            on_text_validate: root.on_textChange()
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: 32
        Label:
            size_hint_x: 1
            id: thresT0
        Slider: 
            size_hint_x: 8
            id: sl0
            value: 128  # スライダの現在の値
            min: 0        # 最小値
            max: 255    # 最大値
            on_touch_move: thres0.text = f"{str(int(self.value))}"   # 値が変化した場合の処理
        TextInput:
            size_hint_x: 1
            id: thres0
            text: '128'
            multiline: False
            on_text_validate: root.on_change_thres(self.text)  # 値を書き換えた場合の処理
''')
 
Window.size = (400,400)
 
class MyWidget(BoxLayout):
    def  open(self):
        self.ids['path0'].text = 'Open Button Pressed!'
    def do_menu(self):
        text = self.ids['sp0'].text
        self.ids['sp0'].text = 'Menu'     # 選択前に戻す
        if text != "Menu":
            self.ids['path0'].text= f"{text} selectted"
    def on_textChange(self):
        print(f"Text Change to \"{self.ids['path0'].text}\"")
 
class MyApp(App):
    def build(self):
        mywidget = MyWidget()
        mywidget.ids['label0'].text = "入力画像"
        mywidget.ids['sp0'].values = ('開く','２階調化','保存')
        return mywidget
 
MyApp().run()