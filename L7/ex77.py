import cv2
import numpy as np
fname = "cat.jpg"   # ←　任意の画像ファイルに変更せよ
# カラー画像としてイメージを読み込み
src = cv2.imread(fname,cv2.IMREAD_COLOR)  # cv2.IMREAD_COLOR = 1
 
# カラー画像をグレイスケール画像へ変換
srcGray = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
 
# グレー画像をガウシアンフィルタで平滑化
srcGray = cv2.GaussianBlur(srcGray,(5,5),1)
 
# ２種類のしきい値処理で2値化
thres = 90
offset = 10

def on_changeX(x):
    global thres
    thres = x
    gosei()
 
def on_changeY(y):
    global offset
    offset = y
    gosei()
 
def gosei():
    ret,img1 = cv2.threshold(srcGray,thres,255,cv2.THRESH_BINARY)
    img2 = cv2.adaptiveThreshold(srcGray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 11, offset)
    img3 = cv2.bitwise_and(img1,img2)
    out = cv2.cvtColor(img3,cv2.COLOR_GRAY2BGR)
    out = cv2.bitwise_and(out,src)
    cv2.imshow("Threshold",img1)
    cv2.imshow("Adaptive",img2)
    cv2.imshow("And",img3)
    cv2.imshow("Image",out)
 
gosei()

cv2.createTrackbar("Threshold","Threshold",thres,255, on_changeX)
cv2.createTrackbar("Offset","Adaptive",offset,20, on_changeY)
  
cv2.waitKey(0)
cv2.destroyAllWindows()