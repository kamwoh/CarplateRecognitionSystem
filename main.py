import cv2
import numpy as np
import time
import sortresult
import own_io
import singleimage
import imageprocess2 as ip2
import charutils as cu
import colorchecking as cc
import sys

##################################################################################
# color constant in bgr
##################################################################################
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
OTSU = 1
NORMAL_OTSU = 3
NORMAL = 2

##################################################################################
# eliminate
##################################################################################
def eliminateSurrounded(characters, display=None):
	indexRemove = set([])
	currentCnt = 0
	for cnt in characters:
		count = 0
		while count < len(characters):
			if count == currentCnt:
				count += 1
				continue
			compareCnt = characters[count]
			if cnt.surround(compareCnt):
				indexRemove.add(count)
			count += 1
		currentCnt += 1
	indexRemove = sorted(indexRemove, reverse=True, key=int)

	for i in indexRemove:
		if display is not None:
			x, y, w, h = characters[i].boundingRect
			cv2.rectangle(display, (x, y), (x+w, y+h), SKYBLUE, 0)
		del characters[i]
	if display is not None:
		cv2.imshow('surrounded_skyblue', display)


def eliminateOverlapped(characters, display=None):
	indexRemove = set([])
	currentCnt = 0
	for cnt in characters:
		count = 0
		while count < len(characters):
			if count == currentCnt:
				count += 1
				continue
			compareCnt = characters[count]
			if compareCnt.overlapCenter(cnt) and cnt.area > compareCnt.area:
				indexRemove.add(count)
			count += 1
		currentCnt += 1

	indexRemove = sorted(indexRemove, reverse=True, key=int)

	for i in indexRemove:
		if display is not None:
			x, y, w, h = characters[i].boundingRect
			cv2.rectangle(display, (x, y), (x+w, y+h), CYAN, 0)
		del characters[i]
	if display is not None:
		cv2.imshow('after_delete_overlapped_cyan', display)


def eliminateArea(characters, display=None):
	indexRemove = set([])
	avgArea = cu.findAvgArea(characters)
	threshArea = avgArea/cu.THRESH_AREA_DENOMINATOR
	count = 0
	for cnt in characters:
		if cnt.area < threshArea:
			indexRemove.add(count)
		count += 1

	indexRemove = sorted(indexRemove, reverse=True, key=int)
	for i in indexRemove:
		if display is not None:
			ip2.drawRect(display, characters[i].boundingRect, PURPLE)
		del characters[i]
	cv2.imshow('after_delete_area_purple', display)


def eliminateDiagonal(characters, display=None):
	indexRemove = set([])
	avgDiagonal = cu.findAvgDiagonal(characters)
	threshDiagonal = avgDiagonal/cu.THRESH_DIAGONAL_DENOMINATOR
	count = 0
	for cnt in characters:
		if cnt.diagonalSize < threshDiagonal:
			indexRemove.add(count)
		count += 1

	indexRemove = sorted(indexRemove, reverse=True, key=int)
	for i in indexRemove:
		if display is not None:
			ip2.drawRect(display, characters[i].boundingRect, YELLOW)
		del characters[i]
	cv2.imshow('after_delete_diagonal_yellow', display)


def eliminateSize(characters, display=None):
	indexRemove = set([])
	currentCount = 0
	for cnt in characters:
		count = 0
		while count < len(characters):
			if count == currentCount:
				count += 1
				continue
			compareCnt = characters[count]
			w1, h1 = cnt.w, cnt.h
			w2, h2 = compareCnt.w, compareCnt.h
			changeInWidth = abs(w2-w1)/float(w2)
			changeInHeight = abs(h2-h1)/float(h2)
			if changeInWidth > cu.MAX_CHANGE_IN_WIDTH:
				if changeInHeight > cu.MAX_CHANGE_IN_HEIGHT:
					if h1 > h2:
						indexRemove.add(currentCount)
					else:
						indexRemove.add(count)
			count += 1
		currentCount += 1

	indexRemove = sorted(indexRemove, reverse=True, key=int)
	for i in indexRemove:
		if display is not None:
			ip2.drawRect(display, characters[i].boundingRect, RED)
		del characters[i]
	cv2.imshow('after_delete_size_red', display)


def eliminateNonMaybe(ori_img, maybeCharacter, total, min_thresh, number, display=None):
	if number is 1:
		thresh_img = ip2.preprocessOtsuThreshold(ori_img)
	elif number is 2:
		thresh_img = ip2.preprocessWithThreshold(ori_img, min_thresh)
	else:
		thresh_img = ip2.preprocessOtsuThreshold(ip2.preprocessWithThreshold(ori_img))
	cu.normalChecking(thresh_img, ori_img, total, 150, display)
	for t in total.getArray():
		if display is not None:
			ip2.drawRect(display, t.boundingRect, MAGENTA)
		maybeCharacter.append(t)


def eliminateNewSize(characters, display=None):
	'''
	eliminate size which small than max change height
	:param characters:
	:param display:
	:return:
	'''
	indexRemove = set([])
	count = 0
	median_h = cu.findMedianHeight(characters)
	for cnt in characters:
		h = cnt.h
		changeInHeight = float(abs(median_h-h))/median_h
		if changeInHeight > cu.MAX_CHANGE_IN_NEW_HEIGHT:
			indexRemove.add(count)
		count += 1
	indexRemove = sorted(indexRemove, reverse=True, key=int)
	for i in indexRemove:
		if display is not None:
			ip2.drawRect(display, characters[i].boundingRect, GREEN)
		del characters[i]
	if display is not None:
		cv2.imshow('new_size_green', display)


def eliminateNewArea(characters, display=None):
	indexRemove = set([])
	count = 0
	median_area = cu.findMedianArea(characters)
	for cnt in characters:
		area = cnt.area
		changeInArea = abs(median_area-area)/median_area
		if changeInArea > cu.MAX_CHANGE_IN_NEW_AREA:
			indexRemove.add(count)
		count += 1
	indexRemove = sorted(indexRemove, reverse=True, key=int)
	for i in indexRemove:
		if display is not None:
			ip2.drawRect(display, characters[i].boundingRect, MAROON)
		del characters[i]

	if display is not None:
		cv2.imshow('new_area_maroon', display)


def eliminateDistance(characters, display=None):
	indexRemove = set([])
	count = 0
	median_distance = cu.findMedianDistance(characters)  # sort by x already
	for i in xrange(len(characters)-1):
		cnt1 = characters[i]
		cnt2 = characters[i+1]
		distance = cnt1.distanceFromCenter(cnt2)
		changeInDistance = abs(distance-median_distance)/median_distance
		if changeInDistance > cu.MAX_CHANGE_IN_DISTANCE:
			indexRemove.add(count)
		count += 1
	indexRemove = sorted(indexRemove, reverse=True, key=int)
	for i in indexRemove:
		if display is not None:
			ip2.drawRect(display, characters[i].boundingRect, INDIGO)
		del characters[i]

	if display is not None:
		cv2.imshow('distance_indigo', display)


def eliminateNewDistance(characters, img, display=None):
	indexRemove = set([])
	count = 0
	newimg = cu.keepCharOnly(characters, img)
	pass


##################################################################################
# find contours
##################################################################################

def findContours(ori_img, number, display=None):
	min_thresh = 150
	maybeCharacter = []
	total = cu.CharArray()
	eliminateNonMaybe(ori_img, maybeCharacter, total, min_thresh, number, display)
	if display is not None:
		cv2.imshow('maybe_white_all_magenta_maybe', display)
	if len(maybeCharacter) != 0:
		cu.sortCharacters(maybeCharacter)
		eliminateNewSize(maybeCharacter, display)
		eliminateNewArea(maybeCharacter, display)
		eliminateSurrounded(maybeCharacter, display)
		eliminateOverlapped(maybeCharacter, display)
		return maybeCharacter
	else:
		return []


##################################################################################
# initialise caffe
##################################################################################
def initCaffe(model, pretrained):
	net = singleimage.initNet(model, pretrained)
	transformer = singleimage.initTransformer(net)
	return net, transformer


##################################################################################
# sort final result
##################################################################################
def sortResult(characterContours, indices, probs=None, flag=cu.SORT_BY_X):
	for i in xrange(len(characterContours)-1, 0, -1):
		maxRes, maxIndex = cu.findMax(characterContours, flag, i+1)
		temp1, temp2 = characterContours[maxIndex], indices[maxIndex]
		characterContours[maxIndex], indices[maxIndex] = characterContours[i], indices[i]
		characterContours[i], indices[i] = temp1, temp2
		if probs is not None:
			temp3 = probs[maxIndex]
			probs[maxIndex] = probs[i]
			probs[i] = temp3

def sortChecking(characters):
	count = 0
	for char in characters:
		for i in xrange(len(characters)):
			if i == count:
				continue
			compareChar = characters[i]
			x1, y1, w1, h1 = char.x, char.y, char.w, char.h
			x2, y2, w2, h2 = compareChar.x, compareChar.y, compareChar.w, compareChar.h
			if y1 < y2 and y2 < y1+h1:
				return True
			if y2 < y1 and y1 < y2+h2:
				return True
		count += 1
	return False

##################################################################################
# main
##################################################################################
def resize(img, thresh_width=300):
	img_height, img_width = img.shape[:2]  # 0 is height, 1 is width
	ratio = thresh_width/float(img_width)
	imgr = cv2.resize(img, (int(ratio*img_width), int(ratio*img_height)), interpolation=cv2.INTER_CUBIC)
	return imgr

def resizeHeight(img, thresh_height=320):
	img_height, img_width = img.shape[:2]  # 0 is height, 1 is width
	ratio = thresh_height/float(img_height)
	imgr = cv2.resize(img, (int(ratio*img_width), int(ratio*img_height)), interpolation=cv2.INTER_CUBIC)
	return imgr

def detectCarplate(cv_image=None, pil_image=None, image_path=None, threshold_method='otsu'):
	'''
	wrapped method to get the result of a car plate
	pseudo:
		convert into cv_image
		then find contours
		process the image into threshold image (only binary color)
		foreach contour image:
		    put into the network
		    save in an array
		sort the array (optional)
		convert to string and return the string
	:param cv_image: image in cv2 form (numpy)
	:param pil_image: image in pil form (Image)
	:param image_path: image path (str)
	:param threshold_method: (best threshold so far)
	:return: a string of car plate number
	'''
	if cv_image is None and pil_image is None and image_path is None:
		raise Exception('one of them must not be None')
	number = 1
	if threshold_method == 'normal':
		number = 2
	if threshold_method == 'normal-otsu':
		number = 3
	if cv_image is not None:
		result = ''
		img = resize(cv_image, 320)
		result_character = findContours(img, number)
		if number == 1:
			currentImg = ip2.preprocessOtsuThreshold(img)
		elif number == 2:
			currentImg = ip2.preprocessWithThreshold(img)
		else:
			currentImg = ip2.preprocessWithThreshold(ip2.preprocessWithThreshold(img))
		for character in result_character: #type: cu.Character
			x, y, w, h = character.boundingRect
			blurredImage = ip2.gaussianBlur(
				ip2.resizeWithSize(ip2.addBorder(ip2.addPadding(currentImg[y:y+h, x:x+w]), 8), (32, 32)), 3)
			caffe_image = singleimage.cv2caffe(blurredImage)
			character.index, character.score = singleimage.getProb(net, caffe_image)
			character.score = character.score[0][character.index]

		result_character = sortresult.sortCarplateResult(result_character)
		for character in result_character:
			result += singleimage.convertIndex(character.index)
			cv2.imwrite('test/'+str(character.index)+'-'+str(character.identity)+'.png', character.getImage(img))

		if len(result) <= 4 and number == 1:
			return detectCarplate(cv_image, threshold_method='normal-otsu')
		elif len(result) <= 4 and number == 3:
			return detectCarplate(cv_image, threshold_method='normal')
		elif len(result) <= 4 and number == 2:
			return result

		return result
	elif pil_image is not None:
		return detectCarplate(cv_image=ip2.PIL2CVImage(pil_image), threshold_method=threshold_method)
	else:
		return detectCarplate(cv_image=cv2.imread(image_path), threshold_method=threshold_method)

def guiRun(file, number):
	'''
	used by gui
	:param file: image path
	:param number: threshold method, 1-'otsu' 2-'threshold' 3-'normal-otsu'
	:return:
	'''
	img = cv2.imread(file)
	if img is not None:
		img = resize(img, 320)
		cv2.imwrite('gui/resize.png', img)
		# display = img.copy()
		characters = findContours(img, number)
		greyscale = ip2.greyscale(img)
		white = cc.newInRangeOfWhite(img)
		threshold = ip2.preprocessWithThreshold(img)
		threshold_otsu = ip2.preprocessOtsuThreshold(img)
		otsu_normal = ip2.preprocessOtsuThreshold(threshold)
		if number == 1:
			contoursImage = threshold_otsu.copy()
			currentImage = threshold_otsu.copy()
		elif number == 2:
			contoursImage = threshold.copy()
			currentImage = threshold.copy()
		else:
			contoursImage = otsu_normal.copy()
			currentImage = otsu_normal.copy()

		contoursImage = ip2.colour(contoursImage)
		indices = []
		scores = []
		for cnt in characters: #type: cu.Character
			x, y, w, h = cnt.boundingRect
			ip2.drawRect(contoursImage, (x, y, w, h), ip2.RED)
			cv_image = ip2.resizeWithSize(ip2.addBorder(ip2.addPadding(currentImage[y:y+h, x:x+w]), 8), (32, 32))
			caffe_image = singleimage.cv2caffe(cv_image)
			prob, score = singleimage.getProb(net, caffe_image)
			cnt.index = int(prob)
			cnt.score = score[0][prob]
			indices.append(int(prob))
			scores.append(score[0][prob])

		# indices, scores = sortResultv2(characters, indices, scores)
		characters = sortresult.sortCarplateResult(characters)
		carplate_str = ''
		for cnt in characters:
			carplate_str += singleimage.convertIndex(cnt.index)

		if len(carplate_str) <= 4 and number == 1:
			return guiRun(file, 3)
		elif len(carplate_str) <= 4 and number == 3:
			return guiRun(file, 2)

		cv2.imwrite('gui/greyscale.png', greyscale)
		cv2.imwrite('gui/white.png', white)
		cv2.imwrite('gui/threshold.png', threshold)
		cv2.imwrite('gui/threshold_otsu.png', threshold_otsu)
		cv2.imwrite('gui/otsu_normal.png', otsu_normal)
		cv2.imwrite('gui/contours.png', contoursImage)
		cv2.imwrite('gui/current.png', currentImage)
		return carplate_str, characters, scores

	else:
		return '', None

##################################################################################
# constant
##################################################################################
caffe_root = 'C:/Users/pc/caffe-windows'
model = caffe_root+'/examples/mnist/lenet.prototxt'  # structure
new_model = caffe_root+'/examples/mnist/lenet_own_input.prototxt'
abc_model = caffe_root+'/examples/mnist/lenet_abc_input.prototxt'
my_model = 'C:/Users/pc/Desktop/carplate_model/carplate_input.prototxt'
my_model_v2 = 'C:/Users/pc/Desktop/deeplearning/carplate_model/carplate_input_0818.prototxt'
my_model_v3 = 'model/carplate_input_060317.prototxt'
pretrained_1 = caffe_root+'/examples/mnist/pretrained_1_original/lenet_iter_10000.caffemodel'  # weight
pretrained_2 = caffe_root+'/examples/mnist/pretrained_2/lenet_iter_10000.caffemodel'  # weight
pretrained_3 = caffe_root+'/examples/mnist/pretrained_3_latest/lenet_iter_10000.caffemodel'  # weight
pretrained_4 = caffe_root+'/examples/mnist/pretrained_4/lenet_iter_10000.caffemodel'  # weight
pretrained_5 = caffe_root+'/examples/mnist/pretrained_5/lenet_own_iter_5000.caffemodel'
pretrained_6 = caffe_root+'/examples/mnist/pretrained_6_new/lenet_new_own_finetune_iter_5000.caffemodel'
pretrained_7 = caffe_root+'/examples/mnist/pretrained_7/lenet_own_abc_iter_10000.caffemodel'
pretrained_7_finetune = caffe_root+'/examples/mnist/pretrained_7_finetune/lenet_finetune_abc_iter_5000.caffemodel'
pretrained_8 = 'C:/Users/pc/Desktop/carplate_model/trained_model/model_iter_30000.caffemodel'
pretrained_9 = 'C:/Users/pc/Desktop/deeplearning/carplate_model/trained_model/model_iter_20000.caffemodel'
pretrained_my_model_v3 = 'model/trained_model/model_iter_5000.caffemodel'
##################################################################################
# init caffe
##################################################################################
#replace your model here
net, transformer = initCaffe(my_model_v2, pretrained_9)
##################################################################################
