import PyQt4.QtGui as QtGui


class Rectangle(QtGui.QGraphicsItem):
    def __init__(self):
        super(Rectangle, self).__init__()

        # self.rect = QtGui.QRectF(0, 0, 200, 40)
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemIsMovable)
