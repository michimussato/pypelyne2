from PyQt4 import QtCore, QtGui
import sys

class Annotator(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.image = None
        self.scale = 1.0
        self.position = (100, 100)

        self.pressed = None
        self.anchor = None

        self.load(r'/Users/michaelmussato/Desktop/pipe.png') #############

    def load(self, filename):
        self.image = QtGui.QImage(filename)

    def mousePressEvent(self, event):
        print 'PRESSED : ',event.pos()
        self.pressed = event.pos()
        self.anchor = self.position

    def mouseReleaseEvent(self, event):
        self.pressed = None

    def mouseMoveEvent(self, event):
        if (self.pressed):
            dx, dy = event.x() - self.pressed.x(), event.y() - self.pressed.y()
            self.position = (self.anchor[0] - dx, self.anchor[1] - dy)
        self.repaint()

    def wheelEvent(self, event):
        oldscale = self.scale
        self.scale += event.delta() / 1200.0
        if self.scale < 0.1:
            self.scale = oldscale

        "unsuccessfully anchors mouse point"
        oldpoint = self.mapFromGlobal(QtGui.QCursor.pos())
        dx, dy = oldpoint.x() - self.position[0], oldpoint.y() - self.position[1]
        newpoint = (oldpoint.x() * (self.scale/oldscale),
                    oldpoint.y() * (self.scale/oldscale))
        self.position = (newpoint[0] - dx, newpoint[1] - dy)

        "successfully anchors top left point"
        #self.position = (self.position[0] * (self.scale / oldscale),
        #                 self.position[1] * (self.scale / oldscale))


        self.repaint()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)

        painter.drawImage(0, 0,
            self.image.scaled(
                self.image.width() * self.scale,
                self.image.height() * self.scale,
                QtCore.Qt.KeepAspectRatio),
            self.position[0], self.position[1])

        painter.end()

app = QtGui.QApplication(sys.argv)
annotator = Annotator()
annotator.show()
sys.exit(app.exec_())