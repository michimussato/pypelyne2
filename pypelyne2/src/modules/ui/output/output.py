import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


# http://trevorius.com/scrapbook/python/pyqt-multiple-inheritance/


class Output(QtGui.QGraphicsItem):
    def __init__(self):
        super(Output, self).__init__()

        # self.setParentItem(parent)

        self.setAcceptHoverEvents(True)

        # self.setFlags(self.ItemIsSelectable)
        # self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)

        self.rect = QtCore.QRectF(-SETTINGS.OUTPUT_RADIUS/2,
                                  -SETTINGS.OUTPUT_RADIUS/2,
                                  SETTINGS.OUTPUT_RADIUS,
                                  SETTINGS.OUTPUT_RADIUS)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(1)

        painter.setPen(pen)

        painter.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0)))

        painter.drawEllipse(self.rect)

    def hoverEnterEvent(self, event):
        print event
