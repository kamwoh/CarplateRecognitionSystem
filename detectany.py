import main
import cv2
import imageprocess2 as ip2
import singleimage
import sortresult

def detectCharacter(file):
	img = cv2.imread(file)
	if img is not None:
		showimg = img.copy()
		result_characters = main.findContours(img, main.OTSU)
		for character in result_characters:
			x, y, w, h = character.boundingRect
			ip2.drawRect(showimg, character.boundingRect, (255,0,255), 10)
			blurredImage = ip2.gaussianBlur(
				ip2.resizeWithSize(ip2.addBorder(ip2.addPadding(img[y:y+h, x:x+w]), 8), (32, 32)), 3)
			caffe_image = singleimage.cv2caffe(blurredImage)
			character.index, character.score = singleimage.getProb(main.net, caffe_image)
			character.score = character.score[0][character.index]

		sortresult.sortCarplateResult(result_characters)
		result = ''
		for character in result_characters:
			char = singleimage.convertIndex(character.index)
			result += char
			ip2.addText(showimg, char, (character.x-30,character.y-30), 20)
			if character.isLastChar:
				result += '\n'

		return result, showimg

