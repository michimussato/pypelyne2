import sys
import os
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import src.conf.settings.SETTINGS as SETTINGS
import src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage
import src.modules.ui.nodegraphicsitem.nodegraphicsitem as nodegraphicsitem
import src.parser.parse_plugins as parse_plugins


app = QtGui.QApplication(sys.argv)

mainwindow = QtGui.QMainWindow()
scene = QtGui.QGraphicsScene()
graphicssview_stage = graphicsview_stage.GraphicsViewStage()
graphicssview_stage.setScene(scene)
mainwindow.setCentralWidget(graphicssview_stage)

plugins = parse_plugins.get_plugins()

for attribute in dir(plugins[0]):
    print '%s = %s' % (attribute, getattr(plugins[1].x64, attribute))

node_graphics_item = nodegraphicsitem.NodeGraphicsItem(position=QtCore.QPoint(0, 0), plugin=plugins[1].x64)
if SETTINGS.NODE_CREATE_COLLAPSED:
    node_graphics_item.expand_layout()

scene.addItem(node_graphics_item)

# if SETTINGS.QSS_ENABLE:
#     with open(os.path.join(SETTINGS.QSS_FILE), 'r') as qss:
#         style = qss.read()
#         app.setStyleSheet(style)

scene = mainwindow
scene.show()
scene.raise_()
app.exec_()