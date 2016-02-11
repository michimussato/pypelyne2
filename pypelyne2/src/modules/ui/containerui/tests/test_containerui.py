import sys
# import uuid
# import os
# import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
# import src.conf.settings.SETTINGS as SETTINGS
# import src.modules.ui.graphicsscene.graphicsscene as graphicsscene
# import pypelyne2.src.modules.ui.graphicsscene.graphicsscenecontainer as graphicsscenecontainer
# import pypelyne2.src.modules.ui.graphicsscene.graphicsscenenodes as graphicsscenenodes
# import pypelyne2.src.modules.ui.nodeui.nodeui as nodeui
import pypelyne2.src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage
import pypelyne2.src.modules.puppeteer.puppeteer as puppeteer
# import pypelyne2.src.modules.ui.nodeui.nodegraphicsitem as nodegraphicsitem
# import pypelyne2.src.modules.ui.portwidget.portwidget as portwidget
# import pypelyne2.src.parser.parse_containers as parse_containers
# import pypelyne2.src.modules.ui.containerui.containerui as containerui
# import pypelyne2.src.parser.parse_plugins as parse_plugins
# import pypelyne2.src.parser.parse_outputs as parse_outputs


app = QtGui.QApplication(sys.argv)

mainwindow = QtGui.QMainWindow()

puppeteer = puppeteer.Puppeteer()

graphicsview_stage = graphicsview_stage.GraphicsViewStage(puppeteer=puppeteer)

mainwindow.setCentralWidget(graphicsview_stage)

nodeui = puppeteer.create_container(scene=graphicsview_stage.scene_object_containers)

puppeteer.create_node(scene=nodeui.nodes_scene)

# graphicsview_stage.scene_object_containers.node_items[0].nodes_scene.create_node()

# print dir(graphicsview_stage.scene_object_container.container_items[0])
#
# container.nodes_scene.create_node()


mainwindow.setCentralWidget(graphicsview_stage)


mainwindow.show()
mainwindow.raise_()
app.exec_()
