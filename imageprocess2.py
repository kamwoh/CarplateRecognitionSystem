import cv2
import numpy as np
import sys
import own_io as io
from PIL import Image, ImageEnhance

MORPH_RECT = cv2.MORPH_RECT
MORPH_CROSS = cv2.MORPH_CROSS
MORPH_ELLIPSE = cv2.MORPH_ELLIPSE
ADAPTIVE_GAUSSIAN = cv2.ADAPTIVE_THRESH_GAUSSIAN_C
ADAPTIVE_MEAN = cv2.ADAPTIVE_THRESH_MEAN_C
THRESH_BINARY = cv2.THRESH_BINARY
THRESH_BINARY_INV = cv2.THRESH_BINARY_INV

PURPLE = (128, 0, 128)
MAGENTA = (255, 0, 255)
DARK_VIOLET = (211, 0, 148)
INDIGO = (130, 0, 75)
WHITE = (255, 255, 255)
RED = (0, 0, 255)
BLACK = (0, 0, 0)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)
ORANGE = (0, 165, 255)
CYAN = (255, 255, 0)
SKYBLUE = (235, 206, 135)
MAROON = (0, 0, 128)
GREY = (128, 128, 128)
SILVER = (192, 192, 192)
NAVY = (0, 0, 128)
DIM_GREY = (105, 105, 105)

R = 'r'
G = 'g'
B = 'b'


class CvImage():
	def __init__(self, **kwargs):
		self.image = kwargs['image']

	def greyscale(self):
		return greyscale(self.image)

	def colour(self):
		return colour(self.image)

	def copy(self):
		return self.image.copy()

	def getCvImage(self):
		return self.image

	def getPILImage(self):
		return PIL2CVImage(self.image)

	def save(self, path):
		io.saveImage(path, self.image)

	@classmethod
	def initFromFile(cls, file_path):
		cv_image = io.readCv2Image(file_path)
		return CvImage(image=cv_image)

	@classmethod
	def initFromCvImage(cls, cv_image):
		return CvImage(image=cv_image)


##################################################################################
# convert format
# PIL to CV
# CV to PIL
##################################################################################
def PIL2CVImage(img):
	newimg = np.array(img)
	if len(newimg.shape) != 2:
		return cv2.cvtColor(newimg, cv2.COLOR_RGB2BGR)
	else:
		return newimg


def CV2PILImage(img):
	if len(img.shape) != 2:
		newimg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		newimg = Image.fromarray(newimg)
	else:
		newimg = Image.fromarray(img)
	return newimg


##################################################################################
# adjust brightness
# adjust contrast
# dilate
# erode
##################################################################################
def adjustBrightness(img, factor):
	if type(img) is np.array or np.ndarray:
		newimg = CV2PILImage(img)
		enhancer = ImageEnhance.Brightness(newimg)
		enhance_img = enhancer.enhance(factor)
		return PIL2CVImage(enhance_img)
	else:
		enhancer = ImageEnhance.Brightness(img)
		enhance_img = enhancer.enhance(factor)
		return enhance_img


def adjustContrast(img, factor):
	if type(img) is np.array or np.ndarray:
		newimg = CV2PILImage(img)
		enhancer = ImageEnhance.Contrast(newimg)
		enhance_img = enhancer.enhance(factor)
		return PIL2CVImage(enhance_img)
	else:
		enhancer = ImageEnhance.Contrast(img)
		enhance_img = enhancer.enhance(factor)
		return enhance_img


def dilate(img, dilate_type=MORPH_RECT, kernel_size=2):
	structuringElement = cv2.getStructuringElement(dilate_type, (kernel_size, kernel_size))
	newimg = cv2.dilate(img, structuringElement)
	return newimg


def erode(img, erode_type=MORPH_RECT, kernel_size=2):
	structuringElement = cv2.getStructuringElement(erode_type, (kernel_size, kernel_size))
	newimg = cv2.erode(img, structuringElement)
	return newimg


def opening(img, opening_type=MORPH_RECT, kernel_size=2):
	structuringElement = cv2.getStructuringElement(opening_type, (kernel_size, kernel_size))
	newimg = cv2.morphologyEx(img, cv2.MORPH_OPEN, structuringElement)
	return newimg


def subtractImage(img1, img2):
	# assert img1.shape != img2.shape, 'shape not same'
	newimg = cv2.subtract(img1, img2)
	return newimg


def addImage(img1, img2):
	# assert img1.shape != img2.shape, 'shape not same'
	newimg = cv2.add(img1, img2)
	return newimg


##################################################################################
# add padding
# place on center
# resize
# difference in size
##################################################################################
def addPadding(img):
	img_height, img_width = img.shape[:2]
	max_size = max(img_width, img_height)
	offset_w = (max_size-img_width)/2
	offset_h = (max_size-img_height)/2
	try:
		newimg = np.zeros((max_size, max_size, img.shape[2]), img.dtype)
	except:
		newimg = np.zeros((max_size, max_size), img.dtype)
	for y in xrange(len(img)):
		for x in xrange(len(img[y])):
			newimg[y+offset_h][x+offset_w] = img[y][x]

	return newimg


def addBorder(cv_image, pixel, border_color=BLACK):
	img_height, img_width = cv_image.shape[:2]
	new_img_height, new_img_width = img_height+pixel*2, img_width+pixel*2
	newimg = placeOnCenter(cv_image, (new_img_width, new_img_height), border_color)
	return newimg


def placeOnCenter(cv_image, size, border_color=BLACK):
	img_height, img_width = cv_image.shape[:2]
	if img_width > size[0] or img_height > size[1]:
		print 'Larger size than '+str(img_width)+'*'+str(img_height)+' pixels'
		return cv_image
	else:
		# if len(cv_image.shape) == 2:
		newimg = np.zeros((size[1], size[0], 3), cv_image.dtype)
		# else:
		#     newimg = np.zeros((size[1], size[0], cv_image.shape[2]), cv_image.dtype)
		offset_w = (size[0]-img_width)/2
		offset_h = (size[1]-img_height)/2
		# grayscale image
		if len(cv_image.shape) == 2:
			cv_image_ = np.tile(cv_image[:, :, np.newaxis], (1, 1, 3))
		else:
			cv_image_ = cv_image
		newimg[offset_h:offset_h+img_height, offset_w:offset_w+img_width] = cv_image_

		if border_color != BLACK:
			newimg[0:newimg.shape[0], 0:offset_w] = border_color
			newimg[0:newimg.shape[0], offset_w+img_width:newimg.shape[1]] = border_color
			newimg[0:offset_h, 0:newimg.shape[1]] = border_color
			newimg[offset_h+img_height:newimg.shape[0], 0:newimg.shape[1]] = border_color
		# for y in xrange(len(cv_image)):
		#     for x in xrange(len(cv_image[y])):
		#         newimg[y+offset_h][x+offset_w] = cv_image[y][x]

		return newimg


def pasteImage(destination_img, paste_img, position):
	img = destination_img.copy()
	paste_img_height, paste_img_width = paste_img.shape[:2]
	paste_img_x, paste_img_y = position
	img[paste_img_y:paste_img_y+paste_img_height, paste_img_x:paste_img_x+paste_img_width] = paste_img[:, :]
	return img


def resizeWithSize(cv_image, size=(28, 28), antialias=True):
	if antialias:
		return cv2.resize(cv_image, size)
	else:
		return cv2.resize(cv_image, size, interpolation=cv2.INTER_NEAREST)
		# newimg_size = size
		# newimg = np.zeros(size,dtype=cv_image.dtype)
		# length_per_pixel = size[0]/cv_image.shape[0]
		# for y in xrange(newimg_size[1]):
		#     for x in xrange(newimg_size[0]):
		#         pass


def resizeWithRatio(cv_image, ratio):
	img_height, img_width = cv_image.shape[:2]
	newimg = cv2.resize(cv_image, (int(ratio*img_width), int(ratio*img_height)), interpolation=cv2.INTER_CUBIC)
	return newimg


def diffSize(cv_image_1, cv_image_2):
	img1_height, img1_width = cv_image_1.shape[:2]
	img2_height, img2_width = cv_image_2.shape[:2]
	return img1_height-img2_height, img1_width-img2_width


def rotate(cv2_image, degree):
	rows, cols = cv2_image.shape[:2]
	M = cv2.getRotationMatrix2D((cols/2, rows/2), degree, 1)
	dst = cv2.warpAffine(cv2_image, M, (cols, rows))
	return dst


##################################################################################
# preprocess image
# binary image
# greyscale
##################################################################################
def binaryImage(img, min):
	newimg = np.copy(img)
	for y in range(img.shape[0]):
		for x in range(img.shape[1]):
			if img[y, x] >= min:
				newimg[y, x] = 255
			else:
				newimg[y, x] = 0
	return newimg


def greyscale(img):
	if len(img.shape) == 3:
		return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	else:
		return img


def colour(img):
	if len(img.shape) == 2:
		return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
	else:
		return img


def BGR2YUV(img):
	if len(img.shape) == 2:
		print 'image must be in bgr or color'
		return None
	else:
		return cv2.cvtColor(img, cv2.COLOR_BGR2YUV)


def removeColor(src_img, colorRemove):
	img = src_img.copy()
	if colorRemove == R:
		img[:, :, 2] = 0
	elif colorRemove == G:
		img[:, :, 1] = 0
	else:
		img[:, :, 0] = 0
	return img


def preprocessWithSpecialThresh(cv_img_src, min_thresh=150):
	if type(cv_img_src) is str:
		cv_img = cv2.imread(cv_img_src)
	else:
		cv_img = cv_img_src
	res, thresh_color = cv2.threshold(cv_img, min_thresh, 255, THRESH_BINARY)
	for y in range(len(thresh_color)):
		for x in range(len(thresh_color[y])):
			r, g, b = thresh_color[y][x]
			if not (r == 255 and g == 255 and b == 255):
				thresh_color[y][x][0] = 0
				thresh_color[y][x][1] = 0
				thresh_color[y][x][2] = 0
	thresh_color = gaussianBlur(thresh_color, 3)
	thresh_color = greyscale(thresh_color)
	res, thresh_color = cv2.threshold(thresh_color, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	return thresh_color

def preprocessWithAdaptiveThresh(src_img, blur_kernel=5, adaptive_method=ADAPTIVE_GAUSSIAN, thresh_type=THRESH_BINARY,
                                 block_size=7, weight=0):
	newimg = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
	newimg = gaussianBlur(newimg, blur_kernel)
	newimg = cv2.adaptiveThreshold(newimg, 255, adaptive_method, thresh_type, block_size, weight)
	return newimg


def preprocessWithThreshold(src_img, min_thresh=150):
	if type(src_img) is str:
		newimg = preprocess(cv2.imread(src_img))
	else:
		newimg = preprocess(src_img)
	res, newimg = cv2.threshold(newimg, min_thresh, 255, THRESH_BINARY)
	return newimg


def erodePreprocessThreshold(src_img, min_thresh, kernel_size=2):
	# print 'enter here'
	newimg = greyscale(src_img)
	res, newimg = cv2.threshold(newimg, min_thresh, 255, THRESH_BINARY)
	# return erode(newimg, kernel_size=kernel_size)
	return newimg

def preprocessOtsuThreshold(src_img):
	if type(src_img) is str:
		newimg = greyscale(cv2.imread(src_img))
	else:
		newimg = greyscale(src_img)
	newimg = erode(newimg, kernel_size=2)
	newimg = gaussianBlur(newimg, 3)
	# newimg = cv2.equalizeHist(newimg)
	# newimg = erode(newimg,kernel_size=5)
	# newimg = erode(newimg,kernel_size=erode_kernel)
	res, newimg = cv2.threshold(newimg, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	return newimg


def preprocess(src_img):
	img = greyscale(src_img)
	structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
	topHat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, structuringElement)
	blackHat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, structuringElement)
	img = cv2.add(img, topHat)
	img = cv2.subtract(img, blackHat)
	return img


'''
bright become brighter
dark become darker
'''


def specialFilter(img):
	pass


##################################################################################
# drawing on img
##################################################################################
def addText(img, text, position, font_size=1):
	# newimg = np.copy(img)
	font = cv2.FONT_HERSHEY_SCRIPT_COMPLEX
	cv2.putText(img, text, position, font, font_size, (255, 255, 255), 1, cv2.CV_AA)
	# return newimg


def drawContours(img, charContours, color, thickness=0):
	for char in charContours:
		drawRect(img, char.boundingRect, color, thickness)


def drawRect(img, rect, color, thickness=0):
	x, y, w, h = rect
	cv2.rectangle(img, (x, y), (x+w, y+h), color, thickness=thickness)


###################################################################################
# histogram utils
###################################################################################
def calcHist(img):
	hist = [0]*256
	newimg = img
	if len(img.shape) == 3:
		newimg = greyscale(img)
	for y in xrange(len(newimg)):
		for x in xrange(len(newimg[y])):
			hist[newimg[y, x]] += 1
	return hist


def equaliseHist(img):
	if len(img.shape) == 3:
		newimg = greyscale(img)
		newimg = cv2.equalizeHist(newimg)
		return newimg
	else:
		return cv2.equalizeHist(img)


# 0 is left right
def calcRegionHist(min_grey_val, img, numberOfRegion, direction):
	if direction == 0:
		size = img.shape[0]/numberOfRegion
		count = [0]*numberOfRegion
		for i in xrange(numberOfRegion):
			for y in xrange(i*size, (i+1)*size):
				for x in xrange(len(img[y])):
					if img[y, x] >= min_grey_val:
						count[i] += 1
		return count
	else:
		size = img.shape[0]/numberOfRegion
		count = [0]*numberOfRegion
		for i in xrange(numberOfRegion):
			for y in xrange(len(img)):
				for x in xrange(i*size, (i+1)*size):
					if img[y, x] >= min_grey_val:
						count[i] += 1
		return count


###################################################################################
# blur utils
###################################################################################
def blur(img, kernel):
	newimg = cv2.blur(img, (kernel, kernel))
	return newimg


def medianBlur(img, kernel):
	newimg = cv2.medianBlur(img, kernel)
	return newimg


def gaussianBlur(img, kernel):
	# sigmaX and sigmaY is standard deviation in X and Y direction
	# sigmaY didn't specify, will be follow sigmaX
	# sigmaX as 0, will be calculated from kernel
	# Gaussian blurring is highly effective in removing gaussian noise from the image
	newimg = cv2.GaussianBlur(img, (kernel, kernel), 0)
	return newimg


###################################################################################
# contours
###################################################################################
def findContours(img, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE):
	contours, hierarchy = cv2.findContours(img, mode, method)
	return contours, hierarchy
