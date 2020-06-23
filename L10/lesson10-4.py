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
    BoxLayout: 
        orientation: 'horizontal'
        BoxLayout: # 入力

            orientation: 'vertical'
            Label:
                size_hint_y: None
                height: 32
                id: label0
                font_size: 20
            Image:
                size_hint_y: 7
                id: pic0
                allow_stretch: True
                source : dummy
        BoxLayout: # 出力
            orientation: 'vertical'
            Label:
                size_hint_y: None
                height: 32
                id: label1
                font_size: 20
            Image:
                size_hint_y: 7
                id: pic1
                allow_stretch: True
                source : dummy
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
            value: 128
            min: 0
            max: 255
            on_touch_move: root.on_change_thres(str(int(self.value)))
        TextInput:
            size_hint_x: 1
            id: thres0
            text: '128'
            multiline: False
            on_text_validate: root.on_change_thres(self.text)
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: 32
        Spinner:
            size_hint_x: None
            width:100
            id: sp0
            text: 'Menu'
            on_text: root.do_menu()
        Label:
            id: path0
            text: './prof.jpg'
''')

import cv2
import numpy as np
dummy = cv2.imread('./prof.jpg',-1)
Window.size = (dummy.shape[1]*2+10,dummy.shape[0]+80)

""" 
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
"""

class MyApp(App):
    def build(self):
        mywidget = MyWidget()
        mywidget.ids['label0'].text = "入力画像"
        mywidget.ids['sp0'].values = ('開く','２階調化','保存')
        mywidget.ids['label1'].text = "出力画像"
        return mywidget

# opencv のカラー画像を kivy テキスチャに変換
def cv2kvtexture(img):
    if len(img.shape) == 2:
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # BGRからRGBへ
    img2 = cv2.flip(img2,0)   # 上下反転
    height = img2.shape[0]
    width = img2.shape[1]
    texture = Texture.create(size=(width,height))
    texture.blit_buffer(img2.tostring())
    return texture

from kivy.graphics.texture import Texture
class MyWidget(BoxLayout):
    mode = 'None'
    def __init__(self,**kwargs):
        super(MyWidget,self).__init__(**kwargs)
        self.srcimg = dummy 
        self.gryimg = self.makegray()
        self.outimg = dummy.copy()
    # ３または４チャネル画像をグレイ化
    def makegray(self):
        img = self.srcimg
        if len(img.shape) == 3 :
            if img.shape[2] == 4: # Alpha チャネル付き
                img = cv2.cvtColor(img,cv2.COLOR_BGRA2GRAY)
            else:
                img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        return img
 
    # 2階調化の後、テクスチャ化
    def threshold(self,thres):
        ret,self.outimg = cv2.threshold(self.gryimg,thres,255,cv2.THRESH_BINARY)
        return cv2kvtexture(self.outimg)
 
    # メニュー処理
    def do_menu(self):
        if self.ids['sp0'].text != 'Menu':
            self.mode = self.ids['sp0'].text
        if self.mode == '２階調化':
            print("Mode", self.mode)
            self.ids['pic1'].texture = self.threshold(128)
 
    def on_change_thres(self,text):
        try: # 整数値が入力されるとは限らないので例外処理
            val = int(text)
        except:
            val = 0 if len(text) == 0 else 128
        val = 0 if val < 0 else (255 if val > 255 else val)
        self.ids['sl0'].value = val
        self.ids['thres0'].text = str(val)
        if self.mode == '２階調化':
            self.ids['pic1'].texture = self.threshold(val)

MyApp().run()