import sys
import PyQt4.QtGui as QtGui
# import PyQt4.QtCore as QtCore
import pypelyne2.src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage


app = QtGui.QApplication(sys.argv)
scene = graphicsview_stage.GraphicsViewStage()
scene_container = graphicsview_stage.GraphicsViewStage()
# rect = QtGui.QRectItem(20,20,20,20)
rect = scene_container.scene_object_containers.addRect(20, 20, 20, 20)

# print dir(rect)

widget_proxy = QtGui.QGraphicsProxyWidget()
widget_proxy.setWidget(scene_container)

scene.scene_object_containers.addItem(widget_proxy)

scene.show()
scene.raise_()
app.exec_()
