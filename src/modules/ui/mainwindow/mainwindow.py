from PyQt4 import QtGui
from PyQt4 import QtCore

import src.modules.ui.dockwidget.dockwidget as dockwidget
import src.modules.ui.dockwidget.dockwidget_graphicsview as dockwidget_graphicsview
import src.modules.ui.dockwidget.dockwidget_tools as dockwidget_tools


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.dock_widget_tools = dockwidget_tools.DockWidgetTools()
        self.dock_widget_bl = dockwidget.DockWidget()
        self.dock_widget_graphicssview = dockwidget_graphicsview.DockWidgetGraphicsView()

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_widget_tools)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_widget_bl)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock_widget_graphicssview)
