from PyQt4 import QtGui

import src.modules.ui.dockwidget.dockwidget as dockwidget
import src.modules.ui.graphicsview.graphicsview as graphicsview


class DockWidgetTools(dockwidget.DockWidget):
    def __init__(self):
        super(DockWidgetTools, self).__init__()
        self.setWindowTitle('DockWidgetTools')
        self.layout = QtGui.QHBoxLayout
        # self.scroll_area = QtGui.QScrollArea()
        #
        # self.scroll_area.setWidget(QtGui.QPushButton())

        # self.btn = QtGui.QPushButton()
        #
        # self.layout.addWidget(self.btn)


        # self.graphicsview = graphicsview.GraphicsView()
