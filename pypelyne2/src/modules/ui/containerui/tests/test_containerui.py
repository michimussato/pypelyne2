import sys
import PyQt4.QtGui as QtGui
import pypelyne2.src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage
import pypelyne2.src.modules.puppeteer.puppeteer as puppeteer


app = QtGui.QApplication(sys.argv)

mainwindow = QtGui.QMainWindow()

puppeteer = puppeteer.Puppeteer()

graphicsview_stage = graphicsview_stage.GraphicsViewStage(puppeteer=puppeteer)

mainwindow.setCentralWidget(graphicsview_stage)

container1 = puppeteer.create_container(scene=graphicsview_stage.scene_object_containers,
                                        container_object='random')
container2 = puppeteer.create_container(scene=graphicsview_stage.scene_object_containers,
                                        container_object='random')
container3 = puppeteer.create_container(scene=graphicsview_stage.scene_object_containers,
                                        container_object='random')

node11 = puppeteer.create_node(scene=container1.container_scene,
                               plugin_object='random')
node21 = puppeteer.create_node(scene=container2.container_scene,
                               plugin_object='random')
node31 = puppeteer.create_node(scene=container3.container_scene,
                               plugin_object='random')

print node11
print node21
print node31

# print container1.container_scene


# mainwindow.setCentralWidget(graphicsview_stage)


mainwindow.show()
mainwindow.raise_()
app.exec_()
