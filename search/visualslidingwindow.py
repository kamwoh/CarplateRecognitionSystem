import slidingwindow
import cv2
import sys
sys.path.insert(0, '.')
import main

path = 'IMG_640.jpg'
img = cv2.imread(path)

for slide in slidingwindow.slidingwindow(img, 100, 100, (320, 200)):
	print main.detectCarplate(slide)
