import logging
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore


class LabelCollapseExpand(QtGui.QLabel):
    def __init__(self):
        super(LabelCollapseExpand, self).__init__()

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on QLabelCollapseExpand ({0})'.format(self))
        if event.button() == QtCore.Qt.RightButton:
            self.emit(QtCore.SIGNAL('clicked'))
        else:
            return QtGui.QLabel.mousePressEvent(self, event)
