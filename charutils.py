import cv2, math, imageprocess2 as ip2, numpy as np, colorchecking as cc
import collider as col, singleimage as si

##################################################################################
# character utils constant
##################################################################################
MIN_ASPECTRATIO = 0.10
MAX_ASPECTRATIO = 1.35
THRESH_AREA_DENOMINATOR = 2.5
THRESH_DIAGONAL_DENOMINATOR = 3.5
SORT_BY_X = 0
INDEX_X = 0
SORT_BY_Y = 1
INDEX_Y = 1
SORT_BY_WIDTH = 2
INDEX_WIDTH = 2
SORT_BY_HEIGHT = 3
INDEX_HEIGHT = 3
RANGE_DISTANCE = 3
MIN_WIDTH = 7
MIN_HEIGHT = 18
MAX_WIDTH = 0
MAX_CHANGE_IN_WIDTH = 0.6
MAX_CHANGE_IN_NEW_WIDTH = 0.4
MAX_CHANGE_IN_HEIGHT = 0.4
MAX_CHANGE_IN_NEW_HEIGHT = 0.2
MAX_CHANGE_IN_NEW_AREA = 0.4
MAX_CHANGE_IN_DISTANCE = 0.4


##################################################################################
# character class
##################################################################################
class Character(object):
	identity_generated = 0

	def __init__(self, contour):
		self.contour = contour
		# self.rotatedRect =
		self.boundingRect = cv2.boundingRect(contour)
		self.x, self.y, self.w, self.h = self.boundingRect
		self.area = self.w*self.h
		self.centerX = (self.x*2+self.w)/2
		self.centerY = (self.y*2+self.h)/2
		self.diagonalSize = math.sqrt(self.w**2+self.h**2)
		self.aspectRatio = float(self.w)/float(self.h)
		self.collider = col.Collider(self)
		self.index = -1
		self.score = 0
		self.identity = Character.identity_generated
		self.isLastChar = False
		Character.identity_generated += 1
		# print Character.identity_generated

	def getCharacter(self):
		if self.index == -1:
			return 'No index assigned'
		return si.convertIndex(self.index)

	def __repr__(self):
		# return str(self.contour)
		return str(self.index)+'-'+si.convertIndex(self.index)

	def __str__(self):
		return str(self.index)+'-'+si.convertIndex(self.index)

	# return str(self.contour)


	def overlapCenter(self, b):
		cx, cy = b.centerX, b.centerY
		x, y, w, h = self.boundingRect
		if x <= cx and cx <= x+w:
			if y <= cy and cy <= y+h:
				return True
		return False

	def overlap(self, b):
		x1, y1, w1, h1 = self.boundingRect
		x2, y2, w2, h2 = b.boundingRect
		if x1 < x2 and x2 < x1+w1:
			if (y1 <= y2 and y2 < y1+h1) or (y1 <= y2+h2 and y2+h2 <= y1+h1):
				return True
		elif x2 <= x1+w1 and x1+w1 < x2+w2:
			if (y1 <= y2 and y2 <= y1+h1) or (y1 <= y2+h2 and y2+h2 <= y1+h1):
				return True
		return False

	def surround(self, b):
		x1, y1, w1, h1 = self.boundingRect
		x2, y2, w2, h2 = b.boundingRect
		if x1 < x2 and x2+w2 < x1+w1:
			if y1 < y2 and y2+h2 < y1+h1:
				return True
		return False

	def differenceSize(self, b):
		w1, h1, area1 = self.w, self.h, self.area
		w2, h2, area2 = b.w, b.h, b.area
		diff_w = abs(w2-w1)
		diff_h = abs(h2-h1)
		diff_area = abs(area2-area1)
		return diff_w, diff_h, diff_area

	def distanceFromCenter(self, b):
		cx1, cy1 = self.centerX, self.centerY
		cx2, cy2 = b.centerX, b.centerY
		diff_x = abs(cx2-cx1)
		diff_y = abs(cy2-cy1)
		distance = math.sqrt(diff_x**2+diff_y**2)
		return distance

	def angleFromCenter(self, b):
		cx1, cy1 = self.centerX, self.centerY
		cx2, cy2 = b.centerX, b.centerY
		opposite = float(abs(cy2-cy1))  # opposite length of triangle
		adjacent = float(abs(cx2-cx1))  # adjacent length of triangle
		if adjacent == 0:  # 90 degree
			radian = float(math.pi/2)
		else:
			radian = math.atan(opposite/adjacent)  # arctan get radian

		angle = radian*(180.0*math.pi)
		return angle

	def setXY(self, new_x, new_y):
		self.x = new_x
		self.y = new_y
		self.centerX = (self.x*2+self.w)/2
		self.centerY = (self.y*2+self.h)/2
		self.boundingRect = self.x, self.y, self.w, self.h

	def isMaybeSize(self):
		'''
		to eliminate impossible size
		:return:
		'''
		if MIN_WIDTH <= self.w and MIN_HEIGHT <= self.h:
			return True
		else:
			return False

	def isMaybeRatio(self):
		'''
		to eliminate impossible ratio
		:return:
		'''
		if MIN_ASPECTRATIO <= self.aspectRatio and self.aspectRatio <= MAX_ASPECTRATIO:
			return True
		else:
			return False

	def getImage(self, img, size=None):
		if size is None:
			return img[self.y:self.y+self.h, self.x:self.x+self.w]
		else:
			start_y = self.y-size
			if start_y < 0:
				start_y = self.y
			end_y = self.y+self.h+size
			if end_y >= img.shape[0]:
				end_y = self.y+self.h
			start_x = self.x-size
			if start_x < 0:
				start_x = self.x
			end_x = self.x+self.w+size
			if end_x >= img.shape[1]:
				end_x = self.x+self.w
			return img[start_y:end_y, start_x:end_x]

	def increaseSize(self, pixel=3):
		self.x -= pixel
		self.y -= pixel
		self.w += pixel
		self.h += pixel
		if self.x < 0:
			self.x = 0
		if self.y < 0:
			self.y = 0

		self.boundingRect = self.x, self.y, self.w, self.h
		self.area = self.w*self.h
		self.centerX = (self.x*2+self.w)/2
		self.centerY = (self.y*2+self.h)/2
		self.diagonalSize = math.sqrt(self.w**2+self.h**2)
		self.aspectRatio = float(self.w)/float(
			self.h)  ##################################################################################


# character array class
##################################################################################
class CharArray(object):
	def __init__(self):
		self.charArray = []

	def __add__(self, new_char, checking=True):
		if checking == True:
			if self.canAdd(new_char):
				self.charArray.append(new_char)
		else:
			self.charArray.append(new_char)

	def sort(self, key=lambda char:char.centerX):
		self.charArray.sort(key=key)

	# def search(self, n):

	def canAdd(self, new_char):
		# for char in self.charArray:
		#     if abs(char.x-x) < 3 and abs(char.y-y) < 3:
		#         return False
		# return True
		for char in self.charArray:
			if abs(char.centerX-new_char.centerX) < 3 and abs(char.centerY-new_char.centerY) < 3:
				return False
		return True

	def getArray(self):
		return self.charArray

	def drawAllChar(self, display, color=ip2.GREEN):
		for char in self.charArray:
			ip2.drawRect(display, char.boundingRect, color)


##################################################################################
# character math utils
##################################################################################
def isCharacter(character):
	if type(character) is Character:
		return True
	else:
		return False


def findMax(characters, flag, endIndex=None):
	max_result = characters[0].boundingRect[flag]
	max_index = 0
	if endIndex is None:
		count = 0
		for character in characters:
			if character.boundingRect[flag] > max_result:
				max_result = character.boundingRect[flag]
				max_index = count
			count += 1
	else:
		for i in xrange(endIndex):
			if characters[i].boundingRect[flag] > max_result:
				max_result = characters[i].boundingRect[flag]
				max_index = i
	return max_result, max_index


def findAvgArea(characters):
	totalArea = 0
	for character in characters:
		totalArea += character.area
	avgArea = float(totalArea)/len(characters)
	return avgArea


def findAvgDiagonal(characters):
	totalDiagonal = 0
	for character in characters:
		totalDiagonal += character.diagonalSize
	avgDiagonal = float(totalDiagonal)/len(characters)
	return avgDiagonal


def findAvgDistance(characters):
	totalDistance = 0
	for i in xrange(len(characters)-1):
		char_1 = characters[i]
		char_2 = characters[i+1]
		totalDistance += char_1.distanceFromCenter(char_2)
	avgDistance = float(totalDistance)/len(characters)
	return avgDistance


def findMinMaxSize(characters):
	maxWidth, maxHeight = characters[0].w, characters[0].h
	minWidth, minHeight = characters[0].w, characters[0].h
	for character in characters:
		if minWidth > character.w:
			minWidth = character.w
		if minHeight > character.h:
			minHeight = character.h
		if maxWidth < character.w:
			maxWidth = character.w
		if maxHeight < character.h:
			maxHeight = character.h
	return maxWidth, maxHeight, minWidth, minHeight


def findMedianWidth(characters):
	sortCharacters(characters, SORT_BY_WIDTH)
	length = len(characters)
	if length == 0:
		return None
	if length%2 == 0:
		index_1 = length/2
		index_2 = index_1-1
		n1 = characters[index_1].w
		n2 = characters[index_2].w
		median = (n1+n2)/2
		return median
	else:
		index_1 = length/2
		median = characters[index_1].w
		return median


def findMedianHeight(characters):
	sortCharacters(characters, SORT_BY_HEIGHT)
	# for char in characters:
	#     print char.h
	length = len(characters)
	if length == 0:
		return None
	if length%2 == 0:
		index_1 = length/2
		index_2 = index_1-1
		n1 = characters[index_1].h
		n2 = characters[index_2].h
		median = (n1+n2)/2
		return median
	else:
		index_1 = length/2
		median = characters[index_1].h
		return median


def findMedianArea(characters):
	characters = sorted(characters, key=lambda Character:Character.area)
	length = len(characters)
	if length == 0:
		return None
	if length%2 == 0:
		index_1 = length/2
		index_2 = index_1-1
		n1 = characters[index_1].area
		n2 = characters[index_2].area
		median = (n1+n2)/2
		return median
	else:
		index_1 = length/2
		median = characters[index_1].area
		return median


def findMedianDiagonal(characters):
	characters = sorted(characters, key=lambda character:character.diagonalSize)
	length = len(characters)
	if length == 0:
		return None
	if length%2 == 0:
		index_1 = length/2
		index_2 = index_1-1
		n1 = characters[index_1].w
		n2 = characters[index_2].w
		median = (n1+n2)/2
		return median
	else:
		index_1 = length/2
		median = characters[index_1].w
		return median


def findMedianDistance(characters):
	sortCharacters(characters)
	distances = []
	for i in xrange(len(characters)-1):
		cnt1 = characters[i]
		cnt2 = characters[i+1]
		distances.append(cnt1.distanceFromCenter(cnt2))
	length = len(distances)
	if length%2 == 0:
		index_1 = length/2
		index_2 = index_1-1
		median = distances[index_1]+distances[index_2]
		median /= 2
		return median
	else:
		index_1 = length/2
		median = distances[index_1]
		return median


##################################################################################
# sorting utils
##################################################################################
def sortCharacters(characters, flag_1=SORT_BY_X):
	if flag_1 == SORT_BY_X:
		characters.sort(key=lambda char:char.centerX)
	elif flag_1 == SORT_BY_Y:
		characters.sort(key=lambda char:char.centerY)
	elif flag_1 == SORT_BY_WIDTH:
		characters.sort(key=lambda char:char.w)
	else:
		characters.sort(key=lambda char:char.h)


##################################################################################
# condition rules
##################################################################################
def recursiveChecking(thresh_img, ori_img, min_thresh, total, offset_x, offset_y):
	if min_thresh <= 180:
		contours, hierarchy = ip2.findContours(thresh_img)
		for cnt in contours:
			char = Character(cnt)
			if char.isMaybeSize():
				if char.aspectRatio >= MAX_ASPECTRATIO:
					crop_img = ori_img[char.y:char.y+char.h, char.x:char.x+char.w]
					crop_img = cc.inRangeOfWhite(crop_img)
					new_thresh_img = ip2.preprocessWithThreshold(crop_img, min_thresh+10)
					recursiveChecking(new_thresh_img, crop_img, min_thresh+10, total, offset_x+char.x, offset_y+char.y)
				else:
					char.setXY(offset_x+char.x, offset_y+char.y)
					# char.increaseSize()
					total.__add__(char)


def normalChecking(thresh_img, ori_img, total, min_thresh, display=None):
	'''
	1. find contours and create cu.Character array
	2. eliminate impossible size character
	:param thresh_img:
	:param ori_img:
	:param total:
	:param min_thresh:
	:param display:
	:return:
	'''
	contours, hierarchy = ip2.findContours(thresh_img)
	for cnt in contours:
		char = Character(cnt)
		if display is not None:
			ip2.drawRect(display, char.boundingRect, ip2.WHITE)
		if char.isMaybeSize():
			if char.aspectRatio <= MAX_ASPECTRATIO:
				# char.increaseSize()
				total.__add__(char)
			# else:
			#     crop_img = ori_img[char.y:char.y+char.h, char.x:char.x+char.w]
			#     new_thresh_img = ip2.preprocessWithThreshold(crop_img, min_thresh)
			#     recursiveChecking(new_thresh_img, crop_img, min_thresh, total, char.x, char.y)


def overlap2contours(left_char, mid_char, right_char):
	if mid_char.overlap(left_char) and mid_char.overlap(right_char):
		return True
	else:
		return False


#################################################################################
#
#################################################################################
def keepCharOnly(characters, img):
	newimg = np.zeros(img.shape)
	for char in characters:
		contour = char.contour
		cv2.drawContours(newimg, contour, -1, ip2.WHITE)
	return newimg
