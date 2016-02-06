import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import logging
import cPickle
import pypelyne2.src.modules.ui.connection.connection as connection
import pypelyne2.src.modules.ui.portwidget.portwidget as portwidget
import pypelyne2.src.modules.ui.nodegraphicsitem.nodegraphicsitem as nodegraphicsitem
import pypelyne2.src.modules.node.node as node
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


# class Container(QtGui.QGraphicsRectItem):
#     def __init__(self, scene_object):
#         super(Container, self).__init__()
#
#         self.scene_object = scene_object
#
#         # self.scene_object.setSceneRect(0, 0, 500, 500)
#
#         self.inputs = Inputs(self.scene_object)
#         self.outputs = Outputs(self.scene_object)
#
#         # print dir(self.scene_object)
#         # print self.scene_object.sceneRect()
#
#         self.setParentItem(self.inputs)
#         self.setParentItem(self.outputs)
#         scene_object.addItem(self.inputs)
#         scene_object.addItem(self.outputs)
#
#     def paint(self, painter, option, widget):
#     #     self.setRect(0, 0, 20, 50)
#         self.setRect(self.scene_object.base_rect.rect())


class Container(QtGui.QGraphicsRectItem):
    def __init__(self, scene_object, view_object):
        super(Container, self).__init__()

        self.setZValue(1000.0)

        self.setAcceptHoverEvents(True)


        self.scene_object = scene_object
        self.view_object = view_object

        # self.container_bar = 20

        self.scene_object.addItem(self)

    def resize(self):
        self.adjust_container()
        # print 'something needs to happen here'


class Inputs(Container):
    def __init__(self, scene_object, view_object):
        super(Inputs, self).__init__(scene_object, view_object)

        self.upstream_nodes = []

        self.outputs = []

        if SETTINGS.AUTO_GENERATE_RANDOM_OUTPUTS:

            for container_input in range(SETTINGS.AUTO_CREATE_CONTAINER_INPUT):
                node_abstract = node.Node()
                self.upstream_nodes.append(node_abstract)

                for i in range(SETTINGS.AUTO_GENERATE_RANDOM_OUTPUTS_COUNT):
                    self.add_output()

    def adjust_container(self):
        self.setRect(2, 1, SETTINGS.CONTAINER_AREA, self.view_object.viewport().height()-3)

        for output_item in self.outputs:
            position = QtCore.QPointF(SETTINGS.CONTAINER_AREA/2,
                                      (self.outputs.index(output_item)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING))+SETTINGS.OUTPUT_OFFSET)
            output_item.setPos(position)

    def add_output(self, output_object=None, port_id=None):
        port = portwidget.Output(node_object=self,
                                 output_object=output_object,
                                 port_id=port_id)
        self.outputs.append(port)
        port.setParentItem(self)
        self.resize()
        # self.outputs_container.setRect(self.viewport().width()-SETTINGS.CONTAINER_AREA-1, 1, SETTINGS.CONTAINER_AREA, self.viewport().height()-3)


        # self.scene_object = scene_object

        # self.setRect(0, 0, 20, 20)

    # def paint(self, painter, option, widget):
    #     print self.scene_object.sceneRect().height()
    #     self.setRect(1, 0, self.bar_width, self.scene_object.sceneRect().height()-10)
    #
    #
    #     pen = QtGui.QPen(QtCore.Qt.SolidLine)
    #     pen.setColor(QtCore.Qt.black)
    #     painter.setPen(pen)
    #     painter.drawRect(self.rect())


class Outputs(Container):
    def __init__(self, scene_object, view_object):
        super(Outputs, self).__init__(scene_object, view_object)

        self.setAcceptDrops(True)

        self.connections = []
        self.upstream_connections = []
        self.inputs = []

        self.setToolTip('drop outputs here to create a container output')

    def adjust_container(self):
        # self.inputs_container.setRect(2, 1, SETTINGS.CONTAINER_AREA, self.viewport().height()-3)

        self.setRect(self.view_object.viewport().width()-SETTINGS.CONTAINER_AREA-1, 1, SETTINGS.CONTAINER_AREA, self.view_object.viewport().height()-3)

        for input_item in self.inputs:
            position = QtCore.QPointF(self.rect().x() + SETTINGS.CONTAINER_AREA/2,
                                      (self.inputs.index(input_item)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING))+SETTINGS.OUTPUT_OFFSET)
            input_item.setPos(position)

    def dragEnterEvent(self, event):
        logging.info('dragEnterEvent on {0}'.format(self))

        if event.mimeData().hasFormat('nodeoutput/draggable-output'):

            data = event.mimeData().data('nodeoutput/draggable-output')
            data = data.data()

            unpickled_output_object = cPickle.loads(data)

            if unpickled_output_object[u'output_graphicsitem_uuid'] in [x.uuid for x in self.inputs]:
                logging.warning('output with uuid {0} {1} is already connected to {2}'.format(unpickled_output_object[u'output_graphicsitem_uuid'],
                                                                                              unpickled_output_object[u'output_object'],
                                                                                              self))
            #     self.set_forbidden()
            #
            # elif self.node.hovered:
            #     self.set_forbidden()
            # else:
            #     self.set_active()

        return QtGui.QGraphicsRectItem.dragEnterEvent(self, event)
        # self.scene_object = scene_object

    def add_input(self, output_object=None, port_id=None, create_connection=True):

        start_item = self.scene_object.find_output_graphics_item(port_id=port_id)

        end_item = portwidget.Input(node_object=self,
                                    output_object=output_object,
                                    port_id=port_id,
                                    start_item=start_item)

        self.inputs.append(end_item)
        end_item.setParentItem(self)

        if create_connection:
            self.add_connection(start_item=start_item, end_item=end_item)

        # self.resize()
        self.adjust_container()

    def add_connection(self, start_item, end_item):
        connection_line = connection.Connection(start_item=start_item,
                                                end_item=end_item,
                                                scene_object=self.scene_object)
        self.connections.append(connection_line)
        self.scene_object.addItem(connection_line)
        self.scene_object.connection_items.append(connection_line)

        start_item.downstream_connections.append(connection_line)
        start_item.downstream_ports.append(end_item)
        end_item.upstream_connections.append(connection_line)

    def dropEvent(self, event):
        logging.info('dropEvent on {0}'.format(self))
        # self.set_inactive()

        if event.mimeData().hasFormat('nodeoutput/draggable-output'):
            event.accept()

            data = event.mimeData().data('nodeoutput/draggable-output')
            data = data.data()

            unpickled_output_object = cPickle.loads(data)

            # self.scene

            self.add_input(output_object=unpickled_output_object[u'output_object'],
                           port_id=unpickled_output_object[u'output_graphicsitem_uuid'])

        else:
            return QtGui.QGraphicsRectItem.dropEvent(self, event)

    # def paint(self, painter, option, widget):
    #     print self.scene_object.sceneRect().height()
    #     self.setRect(70, 0, self.bar_width, self.scene_object.sceneRect().height()-10)
    #
    #     pen = QtGui.QPen(QtCore.Qt.SolidLine)
    #     pen.setColor(QtCore.Qt.black)
    #     painter.setPen(pen)
    #     painter.drawRect(self.rect())
