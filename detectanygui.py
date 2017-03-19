from PyQt4 import QtGui, QtCore
import detectany, sys, cv2

class Window(QtGui.QMainWindow):

	def __init__(self):
		super(Window, self).__init__()
		labelX, labelY, labelWidth, labelHeight = 20,20,500-20-20,500-20-100
		btnX, btnY, btnWidth, btnHeight = 20,500-40,100,40

		self.labelstr = ''
		self.label = QtGui.QLabel(self)
		self.label.setText('text here')
		self.label.setGeometry(labelX, labelY, labelWidth, labelHeight)

		self.btnOpen = QtGui.QPushButton('Open',self)
		self.btnOpen.clicked.connect(self.btnOnClicked)
		self.btnOpen.setGeometry(btnX, btnY, btnWidth, btnHeight)

		self.setGeometry(100,100,500,500)
		self.setWindowTitle('detect any')
		self.show()

	def btnOnClicked(self):
		path = QtGui.QFileDialog.getOpenFileName(self, 'Open file')
		path = str(path)
		if path != '':
			result, showimg = detectany.detectCharacter(path)
			showimg = detectany.main.resize(showimg, 1000)
			cv2.imshow('show', showimg)
			self.label.setText(result)

app = QtGui.QApplication(sys.argv)
w = Window()
sys.exit(app.exec_())