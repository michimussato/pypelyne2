import sys
import PyQt4.QtGui as QtGui
import pypelyne2.src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage
import pypelyne2.src.modules._puppeteer.puppeteer as puppeteer


app = QtGui.QApplication(sys.argv)

mainwindow = QtGui.QMainWindow()


puppeteer = puppeteer.Puppeteer()

graphicsview_stage = graphicsview_stage.GraphicsViewStage(puppeteer=puppeteer)

mainwindow.setCentralWidget(graphicsview_stage)

container1 = puppeteer.create_container(scene=graphicsview_stage.scene_object_containers,
                                        container_object='random')

node11 = puppeteer.create_node(scene=container1.container_scene,
                               plugin_object='random')

node12 = puppeteer.create_node(scene=container1.container_scene,
                               plugin_object='random')

node13 = puppeteer.create_node(scene=container1.container_scene,
                               plugin_object='random')

node14 = puppeteer.create_node(scene=container1.container_scene,
                               plugin_object='random')

outputs = []

for i in range(10):
    output = puppeteer.create_output(node=node11,
                                     output_object='random')

    outputs.append(output)

    # puppeteer should take care of this
    # output_item = puppeteer.find_output_graphics_item(scene=container1.container_scene,
    #                                                   port_id=output.object_id)

    input_item12 = puppeteer.create_input(scene=container1.container_scene,
                                          node=node12,
                                          output_object=output.output_object,
                                          start_port_id=output.object_id)

    input_item13 = puppeteer.create_input(scene=container1.container_scene,
                                          node=node13,
                                          output_object=output.output_object,
                                          start_port_id=output.object_id)

    connection12 = puppeteer.add_connection(scene=container1.container_scene,
                                            start_port_id=output.object_id,
                                            end_item=input_item12)

    connection13 = puppeteer.add_connection(scene=container1.container_scene,
                                            start_port_id=output.object_id,
                                            end_item=input_item13)


for i in range(10):
    output = puppeteer.create_output(node=node13,
                                     output_object='random')

    # # puppeteer should take care of this
    # output_item = puppeteer.find_output_graphics_item(scene=container1.container_scene,
    #                                                   port_id=output.object_id)

    input_item14 = puppeteer.create_input(scene=container1.container_scene,
                                          node=node14,
                                          output_object=output.output_object,
                                          start_port_id=output.object_id)

    connection14 = puppeteer.add_connection(scene=container1.container_scene,
                                            start_port_id=output.object_id,
                                            end_item=input_item14)

for output in outputs:
    # # print i.object_id
    # # puppeteer should take care of this
    # output_item = puppeteer.find_output_graphics_item(scene=container1.container_scene,
    #                                                   port_id=output.object_id)

    input_item14 = puppeteer.create_input(scene=container1.container_scene,
                                          node=node14,
                                          output_object=output.output_object,
                                          start_port_id=output.object_id)

    connection14 = puppeteer.add_connection(scene=container1.container_scene,
                                            start_port_id=output.object_id,
                                            end_item=input_item14)




mainwindow.show()
mainwindow.raise_()
app.exec_()
