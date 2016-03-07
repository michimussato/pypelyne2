import sys

import PyQt4.QtGui as QtGui

import pypelyne2.src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage
# import pypelyne2.src.modules.ui.nodeui.nodeui as nodeui
import pypelyne2.src.modules.core.parser.plugin.parse_plugins as parse_plugins
import pypelyne2.src.modules.puppeteer.puppeteer as puppeteer
# import pypelyne2.src.modules.ui.graphicsscene.graphicsscenenodes as graphicsscenenodes


app = QtGui.QApplication(sys.argv)

mainwindow = QtGui.QMainWindow()

puppeteer = puppeteer.Puppeteer()

# scene = QtGui.QGraphicsScene()
# scene = graphicsscenenodes.GraphicsSceneNodes(puppeteer=puppeteer)
graphicssview_stage = graphicsview_stage.GraphicsViewStage(puppeteer=puppeteer)
# graphicssview_stage.setScene(scene)
mainwindow.setCentralWidget(graphicssview_stage)

plugins = parse_plugins.get_plugins()

for attribute in dir(plugins[0]):
    print '%s = %s' % (attribute, getattr(plugins[1].rand_arck, attribute))

# node_graphics_item_x32 = nodeui.NodeUI(puppeteer=puppeteer)
# node_graphics_item_x64 = nodegraphicsitem.NodeUI(position=QtCore.QPoint(10, 10), plugin=plugins[2].x64)
# node_graphics_item_submitter = nodegraphicsitem.NodeUI(position=QtCore.QPoint(20, 20), plugin=plugins[2].submitter)

# node_graphics_item_x32.collapse_layout()
# node_graphics_item_x64.expand_layout()
# node_graphics_item_submitter.expand_layout()

# print graphicssview_stage.scene_object_containers

puppeteer.create_node(scene=graphicssview_stage.scene_object_containers)

# graphicssview_stage.scene_object_containers.addItem(node_graphics_item_x32)
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
