import sys

import PyQt4.QtGui as QtGui

import src.modules.ui.graphicsview.graphicsview as graphicsview
import src.modules.ui.rectangle.rectangle as rectangle

app = QtGui.QApplication(sys.argv)
# screen_size = QtGui.QApplication.desktop().availableGeometry()
scene = graphicsview.GraphicsView()
# scene.resize(int(screen_size.width()), int(screen_size.height()))
scene.show()
app.exec_()
