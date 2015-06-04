import cv2
import numpy as np

def SingleColorFilter(image,level=230):
	a = [image.shape[0],image.shape[1],1]
	temp = np.zeros(image.shape,np.uint8)
	for i in range(0,image.shape[0]):
		for j in range(0,image.shape[1]):
			counter = 0
			color_temp = 0
			b,g,r = image[i,j]
			if r > level:
				counter += 1
				color_temp = r
			if g > level:
			 	counter += 1
			 	color_temp = g
			if b > level:
			 	counter += 1
			 	color_temp = b
			if counter == 1 :
				temp[i,j] = color_temp

	return temp

img = cv2.imread('b.jpg')
img2 = SingleColorFilter(img,level=220)

cv2.namedWindow('color')
cv2.imshow('color',img2)
cv2.waitKey(0)
cv2.destroyAllWindows()
