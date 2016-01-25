from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.addPixmap(QtGui.QPixmap('image.jpg'))
        self.scene.installEventFilter(self)
        self.view = QtGui.QGraphicsView(self)
        self.view.setScene(self.scene)
        self.label = QtGui.QLabel(self)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.label)

    def eventFilter(self, source, event):
        print source, event

        if (source is self.scene and
            event.type() == QtCore.QEvent.GraphicsSceneMouseRelease and
            event.button() == QtCore.Qt.LeftButton):
            pos = event.scenePos()
            self.label.setText('x=%0.01f,y=%0.01f' % (pos.x(), pos.y()))
        return QtGui.QWidget.eventFilter(self, source, event)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())