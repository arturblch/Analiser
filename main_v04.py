#############################################################################
##
##  This program uses to define the path of the curent
##
#############################################################################


# These are only needed for Python v2 but are harmless for Python v3.

from PyQt4 import QtCore, QtGui


class ScribbleArea(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ScribbleArea, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_StaticContents)
        self.myPenColor = QtGui.QColor(0,255,0) #green
        self.image1 = QtGui.QImage()
        self.image2 = QtGui.QImage()
        self.image_1 = QtGui.QImage()
        self.image_2 = QtGui.QImage()
        self.alpha = 0.5

	#--------------- fill ----------------------

    def fill(self, pos, layer=0, t_col=0xFF000000, bl=0):

        value = bl and QtGui.qRgb(*QtGui.QColor(0,0,0).getRgb()[:-1]) or QtGui.qRgb(*self.myPenColor.getRgb()[:-1])
        img = QtGui.QImage()

        if layer == 0:
            img = self.image1
        elif layer == 1:
            img = self.image2

        img_w = img.width()
        img_h = img.height()
        sw = []
        q = [pos,]
        while(len(q)>0):
            curent=q.pop(0)
            if img.pixel(*curent) == t_col:
                img.setPixel(curent[0],curent[1], value) 
            elif img.pixel(*curent) == 0xFF0000FF:
                print 'Hiii'
                sw.append(curent)
                self.fill(curent,layer,0xFF0000FF)
            direct = [(curent[0]-1,curent[1]),
                      (curent[0]+1,curent[1]),
                      (curent[0],curent[1]+1),
                      (curent[0],curent[1]-1)]
            for dir in direct:
                if  img_w>dir[0]>=0 and img_h>dir[1]>=0 \
                and dir not in q:
                    if img.pixel(dir[0],dir[1]) == t_col:
                        q.append((dir[0],dir[1]))   
                    elif img.pixel(dir[0],dir[1]) == 0xFF0000FF:
                        sw.append(curent)
                        print 'Hiii1'
                        print sw
                        self.fill(curent,layer,0xFF0000FF)

        self.repaint()
        return sw


    #--------------- end fill ------------------
    
    def find(self,pos,start):
        layer = start 				#number of start layer
        sw = self.fill(pos, layer)         #typle for colecting "blue" points
        while (len(sw)>0):
            layer += 1
            for point in sw:
                print point
                print '----Point'
                sw = sw[1:]
                n_pos = self.nearest(point, layer%2)
                if n_pos == 0:
                    continue
                sw += self.fill(n_pos,layer%2)




    def nearest(self, pos, layer):
        img = QtGui.QImage()
        if layer == 0:
            img = self.image1
        elif layer == 1:
            img = self.image2

        img_w = img.width()
        img_h = img.height()
        i = 50
        q = [pos,]
        while(i>0):
            curent=q.pop(0)
            if img.pixel(*curent) == 0xFF0000FF:
                self.fill(curent,layer,0xFF0000FF,1)
                print curent
                print '-------Nearest'
                return curent

            direct = [(curent[0]-1,curent[1]),
                    (curent[0]+1,curent[1]),
                    (curent[0],curent[1]+1),
                    (curent[0],curent[1]-1)]

            for dir in direct: 
                if img_w>dir[0]>=0 and img_h>dir[1]>=0 and dir not in q:
                    if img.pixel(*curent) == 0xFF0000FF:
                        self.fill(curent,layer,0xFF0000FF,1)
                        return curent
                    else:
                        q.append((dir[0],dir[1]))
            i -= 1
        print '-------Nearest ==== 0'
        return 0



    def setalpha(self, event): 
        self.alpha = round(float(event) / 100, 2) 
        self.repaint()
        
    def reset(self):
        self.image1 = QtGui.QImage(self.image_1)
        self.image2 = QtGui.QImage(self.image_2)
        self.repaint()

    def openImage(self, fileName, num):
        loadedImage = QtGui.QImage()
        if not loadedImage.load(fileName):
            return False

        newSize = loadedImage.size().expandedTo(self.size())
        self.resizeImage(loadedImage, newSize)
        if num == 1:
            self.image_1 = loadedImage.convertToFormat(QtGui.QImage.Format_ARGB32_Premultiplied)
            self.image1 = self.image_1.scaledToWidth(720).scaledToHeight(540)
            
        if num == 2:
            self.image_2 = loadedImage.convertToFormat(QtGui.QImage.Format_ARGB32_Premultiplied)
            self.image2 = self.image_2.scaledToWidth(720).scaledToHeight(540)
        self.update()
        
        
        return True
        
    def blackWhite(self):
        img_w = self.width()
        img_h = self.height()
        for i in range(0,img_w):
        	for j in range(0,img_h):
        		if self.image1.pixel(i,j) < 0xFF808080:
        			self.image1.setPixel(i,j, 0xFF000000)
        		else:	
        			self.image1.setPixel(i,j, 0xFFFFFFFF)
        		if self.image2.pixel(i,j) < 0xFF808080:
        			self.image2.setPixel(i,j, 0xFF000000)
        		else:	
        			self.image2.setPixel(i,j, 0xFFFFFFFF)
        	print i
        self.repaint()
        
    
    def setPenColor(self, newColor):
        self.myPenColor = newColor

    def clearImage(self):
        self.image1.fill(QtGui.qRgb(255, 255, 255))
        self.image2.fill(QtGui.qRgb(255, 255, 255))
        self.update()
      

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setOpacity(self.alpha)
        painter.drawImage(event.rect(), self.image1)
        painter.setOpacity(1-self.alpha)
        painter.drawImage(event.rect(), self.image2)


    def resizeEvent(self, event):
        if self.width() > self.image1.width() or self.height() > self.image1.height():
            newWidth = max(self.width() + 128, self.image1.width())
            newHeight = max(self.height() + 128, self.image1.height())
            self.resizeImage(self.image1, QtCore.QSize(newWidth, newHeight))
            self.update()

        super(ScribbleArea, self).resizeEvent(event)


    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.qRgb(255, 255, 255))
        painter = QtGui.QPainter(newImage)
        painter.drawImage(QtCore.QPoint(0, 0), image)
        self.image1 = newImage
        
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            c = self.image1.pixel(event.x(), event.y())
            colors = QtGui.QColor(c).getRgb()
            print "(%s,%s) color= %s" % (event.x(), event.y(), colors)
            self.find((event.x(),event.y()), 0)
            
        if event.button() == QtCore.Qt.RightButton:
            c = self.image2.pixel(event.x(), event.y())
            colors = QtGui.QColor(c).getRgb()
            print "(%s,%s) color= %s" % (event.x(), event.y(), colors)
            self.find((event.x(),event.y()), 1)
            
    def penColor(self):
        return self.myPenColor


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.saveAsActs = []
        central = QtGui.QWidget()
       
        self.scribbleArea = ScribbleArea(central)
        self.scribbleArea.resize(500, 500)
        self.scribbleArea.setGeometry(QtCore.QRect(70, 50, 720, 540))
        self.scribbleArea.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        
        self.hSlider = QtGui.QSlider(central)
        self.hSlider.setValue(50)
        self.hSlider.setGeometry(QtCore.QRect(90, 600, 231, 19))
        self.hSlider.setOrientation(QtCore.Qt.Horizontal)
        
        self.ResButton = QtGui.QPushButton("Reset",central)
        self.ResButton.setGeometry(QtCore.QRect(380, 600, 75, 23)) 
        self.ResButton.setShortcut(QtGui.QKeySequence("Ctrl+R"))
        
        self.setCentralWidget(central)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Scribble")
        self.resize(850, 670)
        
        self.hSlider.valueChanged.connect(self.scribbleArea.setalpha)
        self.ResButton.pressed.connect(self.scribbleArea.reset)
        
    def valChange(self):
        print self.hSlider.value()


    def open(self):
        for i in [1,2]:
            fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                QtCore.QDir.currentPath())
            if fileName:
                self.scribbleArea.openImage(fileName, i)
                print(fileName.fromAscii(fileName,-1))

    def save(self):
        action = self.sender()
        fileFormat = action.data()
        self.saveFile(fileFormat)

    def penColor(self):
        newColor = QtGui.QColorDialog.getColor(self.scribbleArea.penColor())
        if newColor.isValid():
            self.scribbleArea.setPenColor(newColor)

    def about(self):
        QtGui.QMessageBox.about(self, "About Scribble",
                "<p>The <b>Scribble</b> example shows how to use "
                "QMainWindow as the base widget for an application, and how "
                "to reimplement some of QWidget's event handlers to receive "
                "the events generated for the application's widgets:</p>"
                "<p>This program uses to define the path of the curent</p>")

    def createActions(self):
        self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.penColorAct = QtGui.QAction("&Pen Color...", self,
                triggered = self.penColor)

        self.blackWhite = QtGui.QAction("&Black and White", self,
                triggered = self.scribbleArea.blackWhite)
                
        self.clearScreenAct = QtGui.QAction("&Clear Screen", self,
                shortcut="Ctrl+L", triggered = self.scribbleArea.clearImage)

        self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):

        fileMenu = QtGui.QMenu("&File", self)
        fileMenu.addAction(self.openAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        optionMenu = QtGui.QMenu("&Options", self)
        optionMenu.addAction(self.penColorAct)
        optionMenu.addAction(self.blackWhite)
        optionMenu.addSeparator()
        optionMenu.addAction(self.clearScreenAct)

        helpMenu = QtGui.QMenu("&Help", self)
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(optionMenu)
        self.menuBar().addMenu(helpMenu)


        
        

        
        
if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
