import charutils as cu

def _group(result_characters):
	groups = [[],[]]
	return groups

def sortCarplateResult(result_characters):
	'''
	group character by y position
	:param result_characters:
	:type result_characters: list[cu.Character]
	:return: sorted characters
	'''
	#find average height
	if len(result_characters) == 0:
		return result_characters

	average_height = 0
	for character in result_characters: # type: cu.Character
		average_height += character.h
	average_height /= len(result_characters)

	group1 = []
	group2 = []
	for i in range(len(result_characters)):
		for j in range(len(result_characters)):
			if i == j:
				continue
			if _largeDiff(result_characters[i], result_characters[j], average_height, 0.55):
				# todo: improve sorting algorithm
				# if ord(result_characters[i].getCharacter()) < ord(result_characters[j].getCharacter()):
				if result_characters[i].y > result_characters[j].y:
					if not _exists(group1, result_characters[i]) and not _exists(group2, result_characters[i]):
						group1.append(result_characters[i])
					if not _exists(group2, result_characters[j]) and not _exists(group1, result_characters[j]):
						group2.append(result_characters[j])
				else:
					if not _exists(group1, result_characters[j]) and not _exists(group2, result_characters[j]):
						group1.append(result_characters[j])
					if not _exists(group2, result_characters[i]) and not _exists(group1, result_characters[i]):
						group2.append(result_characters[i])

	if len(group1) == 0:
		result_characters.sort(key=lambda char: char.x)
		return result_characters
	else:
		group1.sort(key=lambda char: char.x)
		group1[-1].isLastChar = True
		group2.sort(key=lambda char: char.x)
		group2[-1].isLastChar = True
		group2.extend(group1)
		return group2

def _exists(result_characters, key_character):
	for character in result_characters:
		if character.identity == key_character.identity:
			return True
	return False

def _largeDiff(char1, char2, average, percentage):
	y1 = char1.y
	y2 = char2.y
	absdiff = abs(y1-y2)
	return absdiff > percentage * average

def sortCarplateResultV2(result_characters):
	'''
	given image:
	|-----------------------|
	| _____________________ | <- 3 line
	|                       |
	| _____________________ |
	|                       |
	| _____________________ |
	|                       |
	|-----------------------|
	1. create 3 line collider with x = 0, y = 1~3 * image height/5 , w = image width, h = 2~4 px,
	2. check how many characters the collider has collided with
	3. add those into
	:param result_characters:
	:return:
	'''
	for character in result_characters: #type: cu.Character
		pass

