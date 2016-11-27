from PyQt4 import QtCore, QtGui


class ScribbleArea(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ScribbleArea, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_StaticContents)
        self.myPenColor = QtGui.QColor(0,255,0) #green
        self.image1 = QtGui.QImage()
        self.image2 = QtGui.QImage()
        self.alpha = 0.5

    def openImage(self, fileName, num):
        loadedImage = QtGui.QImage()
        if not loadedImage.load(fileName):
            print 'False'
            return False

        newSize = loadedImage.size().expandedTo(self.size())
        self.resizeImage(loadedImage, newSize)
        if num == 1:
            self.image1 = loadedImage.convertToFormat(QtGui.QImage.Format_ARGB32_Premultiplied)

        if num == 2:
            self.image2 = loadedImage.convertToFormat(QtGui.QImage.Format_ARGB32_Premultiplied)
        self.update()

        print 'Good'
        return True
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(self.alpha)
        painter.drawImage(event.rect(), self.image1)
        painter.setOpacity(1-self.alpha)
        painter.drawImage(event.rect(), self.image2)   
        

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.qRgb(255, 255, 255))
        painter = QtGui.QPainter(newImage)
        painter.drawImage(QtCore.QPoint(0, 0), image)
        self.image1 = newImage

    def resizeEvent(self, event):
        if self.width() > self.image1.width() or self.height() > self.image1.height():
            newWidth = max(self.width() + 128, self.image1.width())
            newHeight = max(self.height() + 128, self.image1.height())
            self.resizeImage(self.image1, QtCore.QSize(newWidth, newHeight))
            self.update()

        super(ScribbleArea, self).resizeEvent(event)

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.saveAsActs = []
        central = QtGui.QWidget()
        self.setWindowTitle("Scribble")

        self.scribbleArea = ScribbleArea(central)
        self.scribbleArea.resize(500, 500)
        self.scribbleArea.setGeometry(QtCore.QRect(70, 50, 720, 540))

        self.setCentralWidget(central)

        self.setWindowTitle("Scribble")
        self.resize(850, 670)

    def open(self):
        fileName1 = u'ТЕСТ1.png'
        fileName2 = u'ТЕСТ2.png'
        self.scribbleArea.openImage(fileName1, 1)
        self.scribbleArea.openImage(fileName2, 2)




if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.open()
    sys.exit(app.exec_())