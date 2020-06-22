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
ret,bimg1 = cv2.threshold(srcGray,thres,255,cv2.THRESH_BINARY)
bimg2 = cv2.adaptiveThreshold(srcGray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 11, offset)
 
# 2つのモノクロ画像を画素ごとの論理積で合成
andimg = cv2.bitwise_and(bimg1,bimg2)
# 結果画像を3プレーン化して入力のカラー画像と合成
andimgBGR = cv2.cvtColor(andimg,cv2.COLOR_GRAY2BGR) 
out = cv2.bitwise_and(andimgBGR,src)
 
cv2.imshow("Threshold",bimg1)
cv2.imshow("Adaptive",bimg2)
cv2.imshow("And",andimg)
cv2.imshow("Image",out)
 
cv2.waitKey(0)
cv2.destroyAllWindows()