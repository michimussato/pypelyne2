from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
import os
import src.conf.settings.SETTINGS as SETTINGS
# import pathlib


class DockWidget(QtGui.QDockWidget):
    def __init__(self):
        super(DockWidget, self).__init__()
        # self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT, 'src', 'modules', 'ui', 'dockwidget', 'dockwidget.ui'), self)
        self.setWindowTitle(str(self))
        self.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
        self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)