# lesson10-60.py
from kivy.app import App
from kivy.lang import Builder 
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.factory import Factory
from kivy.core.text import LabelBase, DEFAULT_FONT 
LabelBase.register(DEFAULT_FONT, "ipaexg.ttf") 
 
import cv2
import numpy as np
import os
 
import filedialog

ORBTHRES = 31

def cv2_imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None
 
def cv2_imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)
 
        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

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
 
dummy = cv2_imread('./prof.jpg',-1)
Window.size = (dummy.shape[1]*2+10,dummy.shape[0]+80)
 
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
 
    # ORB特徴抽出後、テクスチャ化
    def orb(self,edgeThreshold=31):
        orb = cv2.ORB_create(edgeThreshold = edgeThreshold)
        gryimg = cv2.cvtColor(self.srcimg,cv2.COLOR_BGR2GRAY)
        self.outimg = self.srcimg.copy()
        orbkps = orb.detect(gryimg)
        for ip in orbkps:
            pt = (np.round(ip.pt[0]).astype(int),np.round(ip.pt[1]).astype(int))
            rd = np.round(ip.size*0.1).astype(int)
            cv2.circle(self.outimg,pt,rd,(255,0,0),1,8,0)
        return cv2kvtexture(self.outimg)

    # メニュー処理
    def do_menu(self):
        if self.ids['sp0'].text == 'Menu':
            return
        else:
            self.mode = self.ids['sp0'].text
            self.ids['sp0'].text = 'Menu'
        if self.mode == 'ORB特徴抽出':
            ORBTHRES = 31
            self.ids['pic1'].texture = self.orb(edgeThreshold = ORBTHRES)
            self.ids['sl0'].value = ORBTHRES
            self.ids['thres0'].text = str(ORBTHRES)
        if self.mode == '開く':
            self.show_load()
        if self.mode == '保存':
            self.show_save()
 
    def on_change_thres(self,text):
        try: # 整数値が入力されるとは限らないので例外処理
            val = int(text)
        except:
            val = 0 if len(text) == 0 else 31 if self.mode == 'ORB特徴抽出' else 128
        val = 0 if val < 0 else (255 if val > 255 else val)
        self.ids['sl0'].value = val
        self.ids['thres0'].text = str(val)
        if self.mode == 'ORB特徴抽出':
            self.ids['pic1'].texture = self.orb(edgeThreshold = val)
 
    def dismiss_popup(self):
        self._popup.dismiss()
        Window.size = self.keepsize
 
    def show_load(self):
        self.keepsize = Window.size
        Window.size = (600,600)
        content = Factory.LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9,0.9))
        self._popup.open()
 
    def load(self, filepath):
        self.srcimg = cv2_imread(filepath)
        self.outimg = self.srcimg.copy()
        self.gryimg = self.makegray()
        self.ids['pic0'].source = filepath
        self.ids['pic1'].source = filepath
        self.ids['path0'].text = filepath
        self.dismiss_popup()
 
    def show_save(self):
        self.keepsize = Window.size
        Window.size = (600,600)
        content = Factory.SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
 
    def save(self, path, filename):
        path = os.path.join(path, filename)
        path1 = os.path.splitext(path)
        if not path1[1].lower() in ['.png','.jpg']:
            path = path1[0]+'.png'
        self.ids['path0'].text = path
        cv2_imwrite(path,self.outimg)
        self.dismiss_popup()

class MyApp(App):
    def build(self):
        mywidget = MyWidget()
        mywidget.ids['label0'].text = "入力画像"
        mywidget.ids['label1'].text = "出力画像"
        mywidget.ids['sp0'].values = ('開く','ORB特徴抽出','保存')
        mywidget.ids['thresT0'].text = "閾値"
        mywidget.mode = 'ORB特徴抽出'
        return mywidget
 
MyApp().run()