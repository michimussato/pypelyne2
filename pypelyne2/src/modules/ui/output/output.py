import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui


# http://trevorius.com/scrapbook/python/pyqt-multiple-inheritance/


class Rect(QtGui.QGraphicsRectItem):
    def __init__(self, parent=None):
        # super(Test, self).__init__()
        QtGui.QGraphicsRectItem.__init__(self, parent)
        # QtGui.QGraphicsLayoutItem.__init__(self)

        self.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black)))
        self.setBrush(QtGui.QBrush(QtCore.Qt.green))
        self.setRect(0, 0, 40, 20)

        print len(dir(self))


class Layout(QtGui.QGraphicsLayoutItem):
    def __init__(self, parent=None):
        # super(Output, self).__init__()
        QtGui.QGraphicsLayoutItem.__init__(self, parent)


class Output(Rect, Layout):
    def __init__(self, parent=None):
        Layout.__init__(self, parent)
        Rect.__init__(self, parent)
