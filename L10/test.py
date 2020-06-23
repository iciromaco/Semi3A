import cv2
import numpy as np
import time
 
# 画像の読み込み
filename = "prof.jpg"
srcimg = cv2.imread(filename,1) # 1:color, 0:gray, -1:asis
gryimg = cv2.cvtColor(srcimg, cv2.COLOR_BGR2GRAY)
 
# Detector の作成
orb = cv2.ORB_create()
sift = cv2.xfeatures2d.SIFT_create()
 
# 特徴検出
t0 = time.time()
orbkps = orb.detect(gryimg)
t1 = time.time()
print("ORB:{} sec".format(t1-t0))
siftkps = sift.detect(gryimg)
t2 = time.time()
print("SIFT:{} sec".format(t2-t1))
 
# 特徴点の描画
for ip in orbkps:
  pt = (np.round(ip.pt[0]).astype(int),np.round(ip.pt[1]).astype(int))
  rd = np.round(ip.size*0.1).astype(int)
  cv2.circle(srcimg,pt,rd,(255,0,0),1,8,0)
for ip in siftkps:
  pt = (np.round(ip.pt[0]).astype(int),np.round(ip.pt[1]).astype(int))
  rd = np.round(ip.size*0.25).astype(int)
  cv2.circle(srcimg,pt,rd,(0,0,255),1,8,0)
 
cv2.imshow("Feature Detect",srcimg)
cv2.waitKey(0)
cv2.destroyWindow()