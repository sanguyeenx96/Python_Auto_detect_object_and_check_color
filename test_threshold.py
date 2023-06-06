import cv2
import numpy as np

img = cv2.imread('cated.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)
area = int(sum(np.sum(thresh,0))/1000)
nguong = str(area)

print("value nguong:"+ nguong)

cv2.imshow('image', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()
