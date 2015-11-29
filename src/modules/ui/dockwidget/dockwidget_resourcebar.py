from PyQt4 import QtCore
import src.modules.ui.dockwidget.dockwidget as dockwidget
import src.modules.ui.resourcebarwidget.resourcebarwidget as resourcebarwidget


class DockWidgetResourceBar(dockwidget.DockWidget):
    def __init__(self, mainwindow=None):
        super(DockWidgetResourceBar, self).__init__()

        self.mainwindow = mainwindow

        self.setWindowTitle('Resources')

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        # self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable | self.DockWidgetClosable)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self.resourcebar = resourcebarwidget.ResourceBarWidget()

        self.setWidget(self.resourcebar)
