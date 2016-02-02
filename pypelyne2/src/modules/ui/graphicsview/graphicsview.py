import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.QtOpenGL as QtOpenGL


class GraphicsView(QtGui.QGraphicsView):
    def __init__(self):
        super(GraphicsView, self).__init__()
        self.scene = None
        self.visible_rect = None
        self.setTransformationAnchor(self.AnchorUnderMouse)

        self.setViewport(QtOpenGL.QGLWidget(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers)))
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setAcceptDrops(True)

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(60, 60, 60, 255), QtCore.Qt.SolidPattern))
