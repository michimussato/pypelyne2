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

scene.addItem(output)


# item1 = output.Output()
# item2 = output.Output()
#
# print type(item2)
#
# # scene.addItem(item1)
# # scene.addItem(item2)
#
# layout = QtGui.QGraphicsLinearLayout()
# # layout.addItem(item1)
# # layout.addItem(item2)
#
# container = QtGui.QGraphicsWidget()
# # container.
# container.setLayout(layout)
# scene.addItem(container)



# pen = QtGui.QPen()









# plugins = parse_plugins.get_plugins()

# for attribute in dir(plugins[0]):
#     print '%s = %s' % (attribute, getattr(plugins[1].x64, attribute))

# node_graphics_item_x32 = nodegraphicsitem.NodeGraphicsItem(position=QtCore.QPoint(0, 0), plugin=plugins[1].x32)
# node_graphics_item_x64 = nodegraphicsitem.NodeGraphicsItem(position=QtCore.QPoint(10, 10), plugin=plugins[2].x64)
# node_graphics_item_submitter = nodegraphicsitem.NodeGraphicsItem(position=QtCore.QPoint(20, 20), plugin=plugins[2].submitter)

# node_graphics_item_x32.collapse_layout()
# node_graphics_item_x64.expand_layout()
# node_graphics_item_submitter.expand_layout()

# scene.addItem(node_graphics_item_x32)
# scene.addItem(node_graphics_item_x64)
# scene.addItem(node_graphics_item_submitter)

# if SETTINGS.QSS_ENABLE:
#     with open(os.path.join(SETTINGS.QSS_FILE), 'r') as qss:
#         style = qss.read()
#         app.setStyleSheet(style)

scene = mainwindow
scene.show()
scene.raise_()
app.exec_()
