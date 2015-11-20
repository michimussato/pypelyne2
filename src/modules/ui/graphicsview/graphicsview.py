from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import QtOpenGL


class GraphicsView(QtGui.QGraphicsView):
    def __init__(self):
        super(GraphicsView, self).__init__()
        self.scene = None
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setViewport(QtOpenGL.QGLWidget(QtOpenGL.QGLFormat(QtOpenGL.QGL.SampleBuffers)))
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)