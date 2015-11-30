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

    # def dropEvent(self, event):
    #     print event

    # def mousePressEvent(self, event):
    #     print 'mousePress'

    def wheelEvent(self, event):

        print self.visibleRegion().boundingRect()
        print self.rect()
        # print self.mapToScene(QtCore.QRectF(self.visibleRegion().boundingRect())).boundingRect()

        factor = 1.02

        visible_rect = self.mapToScene(self.rect()).boundingRect()
        # visible_rect = QtCore.QRectF(self.rect())
        # visible_rect = self.mapToGlobal(self.rect()).boundingRect()
        # visible_rect = self.mapToScene(self.visibleRegion().boundingRect()).boundingRect()
        self.setSceneRect(visible_rect)

        # self.centerOn(event.pos())

        #print 'event.delta() = %s' %event.delta()

        if event.delta() > 0:
            self.scale(factor, factor)
            # self.scene.centerOn(event.pos())

        else:
            self.scale(1.0 / factor, 1.0 / factor)
            # self.centerOn(event.pos())

        # self.visible_rect = visible_rect

#     def visible
#
#     QRectF XXX::getCurrrentlyVisibleRegion() const
# {
#         //to receive the currently visible area, map the widgets bounds to the scene
#
#         QPointF topLeft = mapToScene (0, 0);
#         QPointF bottomRight = mapToScene (this->width(), this->height());
#
#         return QRectF (topLeft, bottomRight);
# }