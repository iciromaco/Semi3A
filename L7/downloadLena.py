from skimage import io
import cv2
img = io.imread('https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png')
io.imsave("Lenna.png",img)