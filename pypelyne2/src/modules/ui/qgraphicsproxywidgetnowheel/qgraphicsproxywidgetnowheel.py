import logging
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore


class QGraphicsProxyWidgetNoWheel(QtGui.QGraphicsProxyWidget):
    def __init__(self):
        super(QGraphicsProxyWidgetNoWheel, self).__init__()

        self.setAcceptDrops(True)

    def dragMoveEvent(self, event):
        logging.info('dragMoveEvent on QGraphicsProxyWidgetNoWheel ({0})'.format(self))
        return QtGui.QGraphicsProxyWidget.dragMoveEvent(self, event)

    def wheelEvent(self, event):
        logging.info('wheelEvent on QGraphicsProxyWidgetNoWheel ({0})'.format(self))
        event.ignore()

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on QGraphicsProxyWidgetNoWheel ({0})'.format(self))
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()
        mouse_modifiers = QtGui.QApplication.mouseButtons()
        if mouse_modifiers == QtCore.Qt.MidButton \
                or keyboard_modifiers == QtCore.Qt.ControlModifier and mouse_modifiers == QtCore.Qt.LeftButton:
            event.ignore()
            return

        return QtGui.QGraphicsProxyWidget.mouseMoveEvent(self, event)
