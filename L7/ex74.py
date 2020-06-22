import cv2
 
# 修復画像出力用の画像領域を確保し，画像修復を実行
src_img = cv2.imread ("moriMoji.jpg", -1)
mask_img = cv2.imread ("moriMask.jpg", 0)

dst_img = cv2.inpaint (src_img, mask_img, 10, cv2.INPAINT_NS)
 
# 入力，マスク，修復結果画像の表示
cv2.imshow ("Source", src_img)
cv2.imshow ("Mask", mask_img)
cv2.imshow ("Inpaint", dst_img)
 
cv2.waitKey (0)
 
cv2.destroyAllWindows ()