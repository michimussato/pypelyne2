# from PyQt4 import QtGui
# from PyQt4 import QtCore
# from PyQt4 import QtOpenGL

import src.modules.ui.graphicsview.graphicsview as graphicsview
import src.modules.ui.graphicsscene.graphicsscene as graphicsscene
# import src.modules.ui.graphicsscene.graphicsscene as graphicsscene


class GraphicsViewStage(graphicsview.GraphicsView):
    def __init__(self):
        super(GraphicsViewStage, self).__init__()
        self.scene = graphicsscene.GraphicsScene()
        self.setSceneRect(0, 0, 500, 500)