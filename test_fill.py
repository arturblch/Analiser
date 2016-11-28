from PyQt4 import QtCore, QtGui


# 
# 484 56
# 417 81
#
#
class position:
    def __init__(self, x, y):
        self.x_pos = x
        self.y_pos = y

    def x(self):
        return self.x_pos

    def y(self):
        return self.y_pos

class ScribbleArea(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ScribbleArea, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_StaticContents)
        self.myPenColor = QtGui.QColor(0,255,0) #green
        self.image1 = QtGui.QImage()
        self.image2 = QtGui.QImage()
        self.alpha = 0.5

    #--------------- fill ----------------------
    def fill(self, pos):
        value = QtGui.qRgb(*self.myPenColor.getRgb()[:-1])
        print QtGui.QColor.fromRgb(value).getRgb()
        img_w = self.image1.width()
        img_h = self.image1.height()
        q = [(pos.x(),pos.y()),]
        while(len(q)>0):
            curent=q.pop(0)
            if self.image1.pixel(*curent) == 0xFF000000:
                self.image1.setPixel(curent[0],curent[1], value)                 
            direct = [(curent[0]-1,curent[1]),(curent[0]+1,curent[1]),(curent[0],curent[1]+1),(curent[0],curent[1]-1)]
            for dir in direct:
                if img_w>dir[0]>0 and img_h>dir[1]>0 and self.image1.pixel(dir[0],dir[1]) == 0xFF000000 and dir not in q:
                    q.append((dir[0],dir[1]))   
        self.repaint() 
    #--------------- end fill ------------------

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

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            c = self.image1.pixel(event.x(), event.y())
            colors = QtGui.QColor(c).getRgb()
            print "(%s,%s) color= %s" % (event.x(), event.y(), colors)
            
        if event.button() == QtCore.Qt.RightButton:
            c = self.image2.pixel(event.x(), event.y())
            colors = QtGui.QColor(c).getRgb()
            print "(%s,%s) color= %s" % (event.x(), event.y(), colors)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.saveAsActs = []
        self.pos1 = position(484,56)
        self.pos2 = position(417,81)
        central = QtGui.QWidget()
        self.setWindowTitle("Scribble")

        self.scribbleArea = ScribbleArea(central)
        self.scribbleArea.resize(500, 500)
        self.scribbleArea.setGeometry(QtCore.QRect(70, 50, 720, 540))

        self.setCentralWidget(central)

        self.setWindowTitle("Scribble")
        self.resize(850, 670)

    def open(self):
        fileName1 = u'test1.png'
        fileName2 = u'test2.png'
        self.scribbleArea.openImage(fileName1, 1)
        self.scribbleArea.openImage(fileName2, 2)
        self.scribbleArea.fill(self.pos2)




if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.open()
    sys.exit(app.exec_())