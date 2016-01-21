from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.label = QtGui.QLabel(self)
        self.label.setText('Hello World')
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Plain)
        self.label.setMouseTracking(True)
        self.label.installEventFilter(self)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.label)

    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.MouseMove and
            source is self.label):
            pos = event.pos()
            print('mouse move: (%d, %d)' % (pos.x(), pos.y()))
        return QtGui.QWidget.eventFilter(self, source, event)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    window.resize(200, 100)
    sys.exit(app.exec_())