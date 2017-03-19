import sys
import main
import imageprocess2 as ip2
from PyQt4 import QtGui, QtCore
import cv2
import sys

import own_io as io

class Popup(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)

	def selectContours(self, contours):
		pass
# greyscale, white, threshold, contoursImage, carplate_str
class Window(QtGui.QMainWindow):
	resize_path = 'gui/resize.png'
	greyscale_path = 'gui/greyscale.png'
	white_path = 'gui/white.png'
	normal_threshold_path = 'gui/threshold.png'
	otsu_threshold_path = 'gui/threshold_otsu.png'
	normal_otsu_path = 'gui/otsu_normal.png'
	contours_path = 'gui/contours.png'
	current_contours_path = 'gui/current.png'

	def __init__(self):
		super(Window, self).__init__()
		self.img_name = ''
		self.img = None
		self.carplate_str = None
		self.charContours = None
		self.scores = None
		self.initUI()

	def initUI(self):
		# btn1 = QtGui.QPushButton('Button1',self)
		# btn1.clicked()
		# btn1.resize(btn1.sizeHint())
		# btn1.move(50,50)

		btnOpen = QtGui.QPushButton('Open', self)
		btnOpen.clicked.connect(self.displayPic)
		btnOpen.setGeometry(360, 20, 260, 40)

		# btnWhite = QtGui.QPushButton('White', self)
		# btnWhite.clicked.connect(self.whitePic)
		# btnWhite.setGeometry(360, 80, 260, 40)

		btnGreyscale = QtGui.QPushButton('Greyscale', self)
		btnGreyscale.clicked.connect(self.showGreyscale)
		btnGreyscale.setGeometry(360, 80, 260, 40)

		btnThresholdOtsu = QtGui.QPushButton('Otsu Threshold', self)
		btnThresholdOtsu.clicked.connect(self.showOtsuThreshold)
		btnThresholdOtsu.setGeometry(360, 140, 260, 40)

		btnThreshold = QtGui.QPushButton('Normal Threshold', self)
		btnThreshold.clicked.connect(self.showNormalThreshold)
		btnThreshold.setGeometry(360, 200, 260, 40)

		btnKeepContours = QtGui.QPushButton('Normal + Otsu', self)
		btnKeepContours.clicked.connect(self.showNormalOtsu)
		btnKeepContours.setGeometry(360, 260, 260, 40)

		btnContours = QtGui.QPushButton('Contours', self)
		btnContours.clicked.connect(self.showContours)
		btnContours.setGeometry(360, 320, 260, 40)

		btnOri = QtGui.QPushButton('Original', self)
		btnOri.clicked.connect(self.showOri)
		btnOri.setGeometry(360, 380, 260, 40)

		btnSave = QtGui.QPushButton('Save Contours', self)
		btnSave.clicked.connect(self.saveContours)
		btnSave.setGeometry(360, 440, 260, 40)

		btnCreateDir = QtGui.QPushButton('Create Dir', self)
		btnCreateDir.clicked.connect(self.createDir)
		btnCreateDir.setGeometry(360, 500, 260, 40)

		self.outputLabel = QtGui.QLabel(self)
		self.outputLabel.setGeometry(20, 500, 600, 40)
		self.outputLabel.setFont(QtGui.QFont('Times', 15, QtGui.QFont.Bold))

		self.outputLabel_prob = QtGui.QLabel(self)
		self.outputLabel_prob.setGeometry(20, 540, 600, 40)
		self.outputLabel_prob.setFont(QtGui.QFont('Times', 12, QtGui.QFont.Bold))

		self.pic = QtGui.QLabel(self)
		self.pic.setGeometry(20, 20, 320, 300)
		self.compute(Window.resize_path, 1)

		self.contourPic = QtGui.QLabel(self)
		self.contourPic.setGeometry(20, 340, 320, 200)

		self.outputLabel.setText('Output: '+self.carplate_str)

		self.setGeometry(300, 300, 640, 640)
		self.setWindowTitle('Carplate Gui')
		self.show()

	def createDir(self):
		dir_path = QtGui.QFileDialog.getExistingDirectory(self, 'Select Directory')
		if len(dir_path) < 1:
			return
		dir_path = str(dir_path)
		io.generateEmptyFolder(dir_path, 34)

	def showOri(self):
		img = cv2.imread(Window.resize_path)
		if img is not None and img.shape[0] > 320:
			img = main.resizeHeight(img, 320)
		cv2.imwrite(Window.resize_path, img)
		absolutePath = QtCore.QString(Window.resize_path)
		self.pic.setPixmap(QtGui.QPixmap(absolutePath))

	def showGreyscale(self):
		img = cv2.imread(Window.greyscale_path)
		if img is not None and img.shape[0] > 320:
			img = main.resizeHeight(img, 320)
			cv2.imwrite(Window.greyscale_path, img)
		self.pic.setPixmap(QtGui.QPixmap(QtCore.QString(Window.greyscale_path)))

	def showOtsuThreshold(self):
		self.compute(Window.resize_path, 1)
		img = cv2.imread(Window.otsu_threshold_path)
		if img is not None and img.shape[0] > 320:
			img = main.resizeHeight(img, 320)
			cv2.imwrite(Window.otsu_threshold_path, img)
		self.pic.setPixmap(QtGui.QPixmap(QtCore.QString(Window.otsu_threshold_path)))

	def showNormalThreshold(self):
		self.compute(Window.resize_path, 2)
		img = cv2.imread(Window.normal_threshold_path)
		if img is not None and img.shape[0] > 320:
			img = main.resizeHeight(img, 320)
			cv2.imwrite(Window.normal_threshold_path, img)
		self.pic.setPixmap(QtGui.QPixmap(QtCore.QString(Window.normal_threshold_path)))

	def showContours(self):
		img = cv2.imread(Window.contours_path)
		if img is not None and img.shape[0] > 320:
			img = main.resizeHeight(img, 320)
			cv2.imwrite(Window.contours_path, img)
		self.pic.setPixmap(QtGui.QPixmap(QtCore.QString(Window.contours_path)))

	def showNormalOtsu(self):
		self.compute(Window.resize_path, 3)
		img = cv2.imread(Window.normal_otsu_path)
		if img is not None and img.shape[0] > 320:
			img = main.resizeHeight(img, 320)
			cv2.imwrite(Window.normal_otsu_path, img)
		self.pic.setPixmap(QtGui.QPixmap(QtCore.QString(Window.normal_otsu_path)))

	def whitePic(self):
		img = cv2.imread(Window.white_path)
		if img is not None and img.shape[0] > 320:
			img = main.resizeHeight(img, 320)
			cv2.imwrite(Window.white_path, img)
		absolutePath = QtCore.QString(Window.white_path)
		self.pic.setPixmap(QtGui.QPixmap(absolutePath))

	def displayPic(self):
		absolutePath = self.showDialog()
		self.compute(absolutePath, 1)

	def saveContours(self):
		for char in self.charContours:
			charImg = ip2.addPadding(char.getImage(io.readCv2Image(Window.current_contours_path), 5))
			io.saveImage('gui/temp_.png', charImg)
			self.contourPic.setPixmap(QtGui.QPixmap(QtCore.QString('gui/temp_.png')))
			io.delete('gui/temp_.png')
			fname = QtGui.QFileDialog.getSaveFileName(self, 'Save File', 'C:/Users/pc/Desktop/contours/',
			                                          filter='Images (*.png)',
			                                          selectedFilter='Images (*.png)')
			if len(fname) < 1:
				print 'break'
				break
			io.saveImage(str(fname), charImg)
		print 'done', str(self.img_name)

	def showDialog(self):
		fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
		                                          'C:/Users/pc/Dropbox (Siswa)/Dropbox/Nixie Team Folder/wohcode/pythoncode/sublime/pic/car')
		if len(fname) >= 1:
			self.img_name = fname
		return fname

	def compute(self, absolutePath, number):
		if(io.isExists(absolutePath)):
			if len(absolutePath) >= 1:
				self.carplate_str, self.charContours, self.scores = main.guiRun(str(absolutePath), number)
				img = cv2.imread(Window.resize_path)
				if img is not None and img.shape[0] > 320:
					img = main.resizeHeight(img, 320)
					cv2.imwrite(Window.resize_path, img)
				self.img = img
				absolutePath = QtCore.QString(Window.resize_path)
				self.pic.setPixmap(QtGui.QPixmap(absolutePath))
				self.outputLabel.setText('Output: '+self.carplate_str)
				self.outputLabel_prob.setText('Scores: '+str(self.scores))
		# else:path
		# 	path = self.showDialog()
		# 	if str(path) != '':
		# 		self.compute(self.showDialog(), 1)

	def getIndexOfAlphabet(alphabet):
		if type(alphabet) is not str:
			return -1
		alphabet_ = alphabet.upper()
		string = '0123456789ABCDEFGHJKLMNPQRSTUVWXYZ'
		for i, s in enumerate(string):
			if s == alphabet_:
				return i
		return -1


app = QtGui.QApplication(sys.argv)
w = Window()
sys.exit(app.exec_())
