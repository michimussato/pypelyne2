import sys
import uuid
# import os
# import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
# import src.conf.settings.SETTINGS as SETTINGS
# import src.modules.ui.graphicsscene.graphicsscene as graphicsscene
import pypelyne2.src.modules.ui.graphicsscene.graphicsscenecontainer as graphicsscenecontainer
import pypelyne2.src.modules.ui.graphicsscene.graphicsscenenodes as graphicsscenenodes
import pypelyne2.src.modules.ui.nodeui.nodeui as nodeui
import pypelyne2.src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage
# import pypelyne2.src.modules.ui.nodeui.nodegraphicsitem as nodegraphicsitem
# import pypelyne2.src.modules.ui.portwidget.portwidget as portwidget
import pypelyne2.src.parser.parse_containers as parse_containers
import pypelyne2.src.modules.ui.containerui.containerui as containerui
import pypelyne2.src.parser.parse_plugins as parse_plugins
import pypelyne2.src.parser.parse_outputs as parse_outputs


app = QtGui.QApplication(sys.argv)

mainwindow = QtGui.QMainWindow()

graphicssview_stage = graphicsview_stage.GraphicsViewStage()

scene_container = graphicsscenecontainer.GraphicsSceneContainer(view_object=graphicssview_stage)
container_ui = containerui.ContainerUI(container=parse_containers.get_containers()[0], scene_object=scene_container)

scene_node = graphicsscenenodes.GraphicsSceneNodes(view_object=graphicssview_stage, container_object=container_ui)

node = nodeui.NodeUI(plugin=parse_plugins.get_plugins()[0].x64, scene_object=scene_node)
scene_node.addItem(node)
node.add_output(output_object=parse_outputs.get_outputs()[0], port_id=str(uuid.uuid4()))

graphicssview_stage.setScene(scene_container)
mainwindow.setCentralWidget(graphicssview_stage)

scene_container.addItem(container_ui)


scene = mainwindow
scene.show()
scene.raise_()
app.exec_()
