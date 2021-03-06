import sys
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import pypelyne2.src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage
import pypelyne2.src.modules.ui.output.output as output
import pypelyne2.src.modules.ui.nodegraphicsitem.nodegraphicsitem as nodegraphicsitem
import pypelyne2.src.parser.parse_plugins as parse_plugins


app = QtGui.QApplication(sys.argv)

mainwindow = QtGui.QMainWindow()
scene = QtGui.QGraphicsScene()
graphicssview_stage = graphicsview_stage.GraphicsViewStage()
graphicssview_stage.setScene(scene)
mainwindow.setCentralWidget(graphicssview_stage)

output = output.Output()
output.setPos(20, 20)

print type(output)

scene.addItem(output)

print scene.children()

scene = mainwindow
scene.show()
scene.raise_()
app.exec_()
