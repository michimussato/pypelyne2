import sys
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
# import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage
import pypelyne2.src.modules.ui.connection.connection as connection


app = QtGui.QApplication(sys.argv)

mainwindow = QtGui.QMainWindow()
scene = QtGui.QGraphicsScene()
scene.global_scale = 1.0
graphicssview_stage = graphicsview_stage.GraphicsViewStage()
graphicssview_stage.setScene(scene)
mainwindow.setCentralWidget(graphicssview_stage)

rect_src = QtGui.QGraphicsRectItem(0, 0, 10, 10)
rect_src.setFlags(rect_src.ItemIsSelectable | rect_src.ItemIsMovable)
# rect_dst = rect_src.setRect(20,20,30,30)
rect_dst = QtGui.QGraphicsRectItem(200, 30, 10, 10)
rect_dst.setFlags(rect_src.ItemIsSelectable | rect_src.ItemIsMovable)
# scene.addRect(0, 0, 10, 10)
scene.addItem(rect_src)
scene.addItem(rect_dst)

connection_line = connection.Connection(start_item=rect_src, end_item=rect_dst, scene_object=scene)

# print type(connection_line)

scene.addItem(connection_line)

scene = mainwindow
scene.show()
scene.raise_()
app.exec_()
