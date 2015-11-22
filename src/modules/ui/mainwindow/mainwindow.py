from PyQt4 import QtGui
from PyQt4 import QtCore

import src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage

import src.modules.ui.dockwidget.dockwidget as dockwidget
import src.modules.ui.dockwidget.dockwidget_plugins as dockwidget_plugins


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.dock_widget_tools = dockwidget_plugins.DockWidgetPlugins()
        self.dock_widget_bl = dockwidget.DockWidget()
        self.graphicssview_stage = graphicsview_stage.GraphicsViewStage()

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_widget_tools)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_widget_bl)

        self.setCentralWidget(self.graphicssview_stage)
