import src.modules.ui.dockwidget.dockwidget as dockwidget
import src.modules.ui.graphicsview.graphicsview as graphicsview


class DockWidgetGraphicsView(dockwidget.DockWidget):
    def __init__(self):
        super(DockWidgetGraphicsView, self).__init__()
        self.setWindowTitle('DockWidgetGraphicsView')
        self.graphicsview = graphicsview.GraphicsView()
