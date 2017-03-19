import charutils as cu


class Collider(object):
	def __init__(self, character=None, boundingRect=None):

		if character is not None:
			self.character = character  # type: cu.Character
			self.x, self.y, self.w, self.h = self.character.boundingRect
		elif boundingRect is not None:
			self.x, self.y, self.w, self.h = boundingRect
		else:
			raise Exception('character or boundingRect must not be None')
		self.x0, self.x1 = self.x, self.x+self.h
		self.y0, self.y1 = self.y, self.y+self.w
		# self.vertices = [Vector2D(x0, y0), Vector2D(x0, y1), Vector2D(x1, y0), Vector2D(x1, y1)]

	def addCollidedCharacter(self, character):
		if self.character is None:
			raise Exception('this is for line collider only')
		if self.collided_characters is None:
			self.collided_characters = []
		self.collided_characters.append(character)

	def equalCollidedCharacter(self, line_collider):
		if self.character is None:
			raise Exception('this is for line collider only')


		for char in self.collided_characters:
			pass # todo: check equal

	def isCollided(self, other_collider):  # type: Collider
		return self.x0 <= other_collider.x1 and self.x1 >= other_collider.x0 and self.y0 <= other_collider.y1 and self.y1 >= other_collider.y0

class Vector2D(object):
	def __init__(self, x=0, y=0):
		self.x, self.y = x, y

	def isGreaterX(self, other_1):
		return self.x >= other_1.x

	def isGreaterY(self, other_1):
		return self.y >= other_1.y

	def isInBetweenX(self, other_1, other_2):
		return (other_1.x >= self.x and self.x >= other_2.x) or (other_2.x >= self.x and self.x >= other_1.x)

	def isInBetweenY(self, other_1, other_2):
		return (other_1.y >= self.y and self.y >= other_2.y) or (other_2.y >= self.y and self.y >= other_1.y)

	def isInBetween(self, other_1, other_2):
		return self.isInBetweenX(other_1, other_2) and self.isInBetweenY(other_1, other_2)
	# def __gt__(self, otherVector2D): # type: Vector2D
	# 	'''
	# 	expression >
	# 	:param otherVector2D: vector to be compared
	# 	:return: true if this.x and this.y larger than otherVector2D
	# 	'''
	# 	return self.x > otherVector2D.x and self.y > otherVector2D.y
	#
	# def __ge__(self, otherVector2D):
	# 	return (self.x >= otherVector2D.x or self.y >= otherVector2D.y) and self.__gt__(otherVector2D)
	#
	# def __lt__(self, other):