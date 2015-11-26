from PyQt4 import QtGui
from PyQt4 import QtCore

import src.conf.settings.SETTINGS as SETTINGS
import src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage
import src.modules.ui.dockwidget.dockwidget as dockwidget
import src.modules.ui.dockwidget.dockwidget_plugins as dockwidget_plugins


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.splash = None
        self.setup_splash_screen()

        # self.splash.show()
        # self.processEvents()
        self.dock_widget_tools = dockwidget_plugins.DockWidgetPlugins()
        self.dock_widget_bl = dockwidget.DockWidget()
        self.graphicssview_stage = graphicsview_stage.GraphicsViewStage()

        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_widget_tools)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_widget_bl)

        self.setCentralWidget(self.graphicssview_stage)

        self.graphicssview_stage.scene.addRect(QtCore.QRectF(0, 0, 512, 512), QtCore.Qt.red)

        self.splash.finish(self.splash)

        # self.raise_()

    def setup_splash_screen(self):
        self.splash = QtGui.QSplashScreen(QtGui.QPixmap(SETTINGS.SPLASH_ICON), QtCore.Qt.WindowStaysOnTopHint)
        self.splash.setMask(self.splash.mask())
        self.splash.show()

    def resizeEvent(self, event):
        self.graphicssview_stage.setSceneRect(0, 0, self.graphicssview_stage.width(), self.graphicssview_stage.height())

    def graphicssview_stage_wheelEvent(self, event):
        factor = 1.41 ** ((event.delta()*.5) / 240.0)
        self.graphicssview_stage.scale(factor, factor)
