import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage
import pypelyne2.src.modules.ui.dockwidget.dockwidget_plugins as dockwidget_plugins
import pypelyne2.src.modules.ui.dockwidget.dockwidget_resourcebar as dockwidget_resourcebar
import pypelyne2.src.modules.ui.dockwidget.dockwidget_output_channels as dockwidget_output_channels
import pypelyne2.src.modules.ui.dockwidget.dockwidget_containers as dockwidget_containers
import pypelyne2.src.modules.puppeteer.puppeteer as puppeteer


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.puppeteer = puppeteer.Puppeteer()

        if SETTINGS.SPLASH:
            self.splash = None
            self.setup_splash_screen()

        self.dock_output_widgets = []

        self.setAnimated(SETTINGS.DOCK_ANIMATED)
        self.setDockNestingEnabled(SETTINGS.DOCK_NESTING)

        self.graphicssview_stage = graphicsview_stage.GraphicsViewStage(puppeteer=self.puppeteer)

        self.dock_widget_plugins = dockwidget_plugins.DockWidgetPlugins(mainwindow=self)
        self.dock_widget_output_channels = dockwidget_output_channels.DockWidgetOutputChannels(mainwindow=self)
        self.resource_bar_widget = dockwidget_resourcebar.DockWidgetResourceBar(mainwindow=self)
        self.dock_widget_containers = dockwidget_containers.DockWidgetContainers(mainwindow=self)

        if SETTINGS.SHOW_PLUGINS:
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_widget_plugins)
        if SETTINGS.SHOW_OUTPUT_CHANNELS:
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock_widget_output_channels)
        if SETTINGS.SHOW_RESOURCES:
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.resource_bar_widget)
        if SETTINGS.SHOW_CONTAINERS:
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock_widget_containers)

        # if SETTINGS.SHOW_PLAYER:
        #     pass

        self.setCentralWidget(self.graphicssview_stage)

        # self.graphicssview_stage.scene.addRect(QtCore.QRectF(0, 0, 512, 512), QtCore.Qt.red)

        if SETTINGS.SPLASH:
            self.splash.finish(self.splash)

    def setup_splash_screen(self):
        self.splash = QtGui.QSplashScreen(QtGui.QPixmap(SETTINGS.SPLASH_ICON), QtCore.Qt.WindowStaysOnTopHint)
        self.splash.setMask(self.splash.mask())
        self.splash.show()

    # def resizeEvent(self, event):
    #     print event
    #     # self.graphicssview_stage.setScen
    #     self.graphicssview_stage.setSceneRect(0, 0, self.graphicssview_stage.width(), self.graphicssview_stage.height())
    #     # print self.graphicssview_stage.sceneRect().width()
    #     # print self.graphicssview_stage.sceneRect().height()
    #
    #     print self.graphicssview_stage.rect()
    #
    #     # self.graphicssview_stage.scene.setSceneRect(self.graphicssview_stage.rect())
    #     self.graphicssview_stage.scene.base_rect.setRect(QtCore.QRectF(self.graphicssview_stage.rect()))
