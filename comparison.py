from PyQt4 import QtGui, QtCore
import sys, imageprocess2 as ip2, cv2


def resize(img, thresh_width=300):
	img_height, img_width = img.shape[:2]  # 0 is height, 1 is width
	ratio = thresh_width/float(img_width)
	imgr = cv2.resize(img, (int(ratio*img_width), int(ratio*img_height)), interpolation=cv2.INTER_CUBIC)
	return imgr


class Window(QtGui.QMainWindow):
	def __init__(self):
		super(Window, self).__init__()

		self.sliderValue = 2
		self.thresh = 150
		self.ori_path = ''
		btnOpenX, btnOpenY, btnOpenWidth, btnOpenHeight = 680, 750, 100, 40

		btnOpen = QtGui.QPushButton('Open', self)
		btnOpen.clicked.connect(self.displayPic)
		btnOpen.setGeometry(btnOpenX, btnOpenY, btnOpenWidth, btnOpenHeight)

		# self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
		# self.slider.setGeometry(10, btnOpenY, 100, 50)
		# self.slider.setMinimum(1)
		# self.slider.setMaximum(10)
		# self.slider.setValue(self.sliderValue)
		# self.slider.setTickPosition(QtGui.QSlider.TicksBelow)
		# self.slider.setTickInterval(2)
		# self.slider.valueChanged.connect(self.onSliderValueChanged)

		self.slider = QtGui.QLineEdit(self)
		self.slider.setText(str(self.sliderValue))
		self.slider.returnPressed.connect(self.adjustKernel)
		self.slider.setGeometry(10, btnOpenY, 100, 50)

		self.textBox = QtGui.QLineEdit(self)
		self.textBox.setText(str(self.thresh))
		self.textBox.returnPressed.connect(self.adjustTextBox)
		self.textBox.setGeometry(260, btnOpenY, 100, 50)
		# geometry parameter: x, y, width, height
		frameX, frameY, frameWidth, frameHeight = 100, 100, 800, 800
		picWidth, picHeight, labelWidth, labelHeight = 400, 400, 100, 10
		x, y = 10, 10

		add = 340
		self.ori = QtGui.QLabel(self)
		self.ori_label = QtGui.QLabel(self)
		self.ori_label.setText('ori image')
		self.ori_label.setGeometry(x, y-10, labelWidth, labelHeight)
		self.ori.setGeometry(x, y, picWidth, picHeight)

		self.compare1 = QtGui.QLabel(self)
		self.compare1_label = QtGui.QLabel(self)
		self.compare1_label.setText('threshold image')
		self.compare1_label.setGeometry(x+add, y-10, labelWidth, labelHeight)
		self.compare1.setGeometry(x+add, y, picWidth, picHeight)

		self.compare2 = QtGui.QLabel(self)
		self.compare2_label = QtGui.QLabel(self)
		self.compare2_label.setText('otsu image')
		self.compare2_label.setGeometry(x-10, y-10+add, labelWidth, labelHeight)
		self.compare2.setGeometry(x, y+add, picWidth, picHeight)

		self.compare3 = QtGui.QLabel(self)
		self.compare3_label = QtGui.QLabel(self)
		self.compare3_label.setText('special image')
		self.compare3_label.setGeometry(x+add, y-10+add, labelWidth, labelHeight)
		self.compare3.setGeometry(x+add, y+add, picWidth, picHeight)

		self.setGeometry(frameX, frameY, frameWidth, frameHeight)
		self.setWindowTitle('comparison')
		self.show()

	def onSliderValueChanged(self):
		parse = int(self.slider.value())
		self.sliderValue = parse
		self.compute(thresh=self.thresh, selection=2)
		# self.textBox.setText(str(parse))

	def adjustKernel(self):
		parse = int(self.slider.text())
		self.sliderValue = parse
		self.compute(thresh=self.thresh, selection=2)

	def adjustTextBox(self):
		try:
			parse = int(self.textBox.text())
			if parse >= 255:
				parse = 255
			elif parse < 0:
				parse = 0
			self.compute(parse)
			self.thresh = parse
		except:
			pass

	def compute(self, thresh=150, selection = 1):
		ori_path = self.ori_path
		if ori_path == '':
			return

		save_path = 'temp.png'
		compare1_img = None
		compare2_img = None
		compare3_img = None
		if selection == 1:
			compare1_img = ip2.preprocessWithThreshold(resize(cv2.imread(ori_path), 320), thresh)
			compare3_img = ip2.preprocessWithSpecialThresh(resize(cv2.imread(ori_path), 320), thresh)
		if selection == 1 or selection == 2:
			compare2_img = ip2.erodePreprocessThreshold(resize(cv2.imread(ori_path), 320), thresh, self.sliderValue)
			print 'enter here'

		if compare1_img is not None:
			cv2.imwrite(save_path, compare1_img)
			self.compare1.setPixmap(QtGui.QPixmap(QtCore.QString(save_path)))

		cv2.imwrite(save_path, compare2_img)
		self.compare2.setPixmap(QtGui.QPixmap(QtCore.QString(save_path)))

		if compare3_img is not None:
			cv2.imwrite(save_path, compare3_img)
			self.compare3.setPixmap(QtGui.QPixmap(QtCore.QString(save_path)))

	def displayPic(self):
		ori_path = str(self.showDialog())
		if ori_path == '':
			return
		self.ori_path = ori_path

		save_path = 'temp.png'
		# ori image
		cv2.imwrite(save_path, resize(cv2.imread(ori_path), 230))
		self.ori.setPixmap(QtGui.QPixmap(QtCore.QString(save_path)))

		self.compute(self.thresh)

	# self.compare1.setPixmap(QtGui.QPixmap(QtCore.QString()))
	# print self.absolutePath

	def showDialog(self):
		fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
		                                          'C:/Users/pc/Dropbox (Siswa)/Dropbox/Nixie Team Folder/wohcode/pythoncode/sublime/pic/car')
		return fname


app = QtGui.QApplication(sys.argv)
w = Window()
sys.exit(app.exec_())
