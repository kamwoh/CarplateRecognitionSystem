import cv2, numpy as np
# import sys
# sys.path.append(0, '/.')
# import imageprocess2 as ip2

def slidingwindow(input_img, slide_x, slide_y, size=(320,240)):
	'''

	:param input_img: input image with width of 640
	:type input_img: np.ndarray
	:param slide_x: gap x between 2 slides
	:param slide_y: gap y between 2 slides
	:param size: return image size
	:return: 320 x 240 slides
	'''
	img_height, img_width = input_img.shape[:2]
	slide_width, slide_height = size
	for y in xrange(0,img_height-slide_height,slide_y):
		for x in xrange(0,img_width-slide_width,slide_x):
			yield input_img[y:y+slide_height,x:x+slide_width]

