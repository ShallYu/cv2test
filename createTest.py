import cv2
import numpy as np
img = cv2.imread("./a.jpg")
emptyImage = np.zeros(img.shape,np.uint8)
emptyImage2 = img.copy()
cv2.imwrite("./b.jpg",emptyImage2,[int(cv2.IMWRITE_JPEG_QUALITY), 5])
