from PyQt4 import QtGui
from PyQt4 import QtCore


class DockWidget(QtGui.QDockWidget):
    def __init__(self):
        super(DockWidget, self).__init__()
        self.setWindowTitle('DockWidget')
