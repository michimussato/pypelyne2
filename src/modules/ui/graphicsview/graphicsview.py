from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtOpenGL

# import src.modules.ui.graphicsscene.graphicsscene as graphicsscene


class GraphicsView(QtGui.QGraphicsView):
    def __init__(self):
        super(GraphicsView, self).__init__()
        self.scene = None
        self.visible_rect = None
        # self.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setTransformationAnchor(self.AnchorUnderMouse)

        self.setViewport(QtOpenGL.QGLWidget(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers)))
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setAcceptDrops(True)

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(60, 60, 60, 255), QtCore.Qt.SolidPattern))

        # self.focus_all_elements()

    # def wheelEvent(self, event):
    #     factor = 1.02
    #
    #     if event.delta() > 0:
    #         self.scale(factor, factor)
    #     else:
    #         self.scale(1.0 / factor, 1.0 / factor)
    #
    #     print self.mapToScene(self.rect()).size()

    # def focus_all_elements(self):
    #     extra_margin = 20
    #     items_rect = self.scene.itemsBoundingRect()
    #     coords = items_rect.getCoords()
    #     new_top_left = QtCore.QPoint(coords[0]-extra_margin, coords[1]-extra_margin)
    #     new_bottom_right = QtCore.QPointF(coords[2]+extra_margin, coords[3]+extra_margin)
    #     new_rect = QtCore.QRectF(new_top_left, new_bottom_right)
    #     self.setSceneRect(new_rect)
    #     self.fitInView(self.sceneRect(), QtCore.Qt.KeepAspectRatio)
    #
    # def mouseDoubleClickEvent(self, event):
    #     self.focus_all_elements()


