import cv2
 
thres = 128
 
image = cv2.imread("Lenna.png",1)
 
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
ret,gray = cv2.threshold(gray,thres,255,cv2.THRESH_BINARY)
 
cv2.imshow("Bin",gray)
cv2.waitKey(0)
cv2.destroyWindow("Bin")