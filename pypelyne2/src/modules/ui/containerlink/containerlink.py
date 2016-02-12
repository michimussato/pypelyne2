import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import logging
import cPickle
import pypelyne2.src.modules.ui.connection.connection as connection
import pypelyne2.src.modules.ui.portwidget.portwidget as portwidget
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
# import pypelyne2.src.modules.ui.containerui.containerui as containerui


class ContainerLink(QtGui.QGraphicsRectItem):
    def __init__(self, scene_object, view_object):
        super(ContainerLink, self).__init__()

        self.setZValue(1000.0)

        self.setAcceptHoverEvents(True)

        self.scene_object = scene_object
        self.container_object = self.scene_object.container_object
        self.view_object = view_object

        self.scene_object.addItem(self)

    def resize(self):
        self.adjust_container()


class ContainerLabel(ContainerLink):
    def __init__(self, scene_object, view_object):
        super(ContainerLabel, self).__init__(scene_object, view_object)

        self.text = QtGui.QGraphicsTextItem()
        self.text.setParentItem(self)
        # print dir(self)
        self.text.setPlainText('container: {0}'.format(self.scene_object.container_object.name_string))

    def resize(self):
        self.adjust_container()

    def adjust_container(self):
        self.setRect(SETTINGS.CONTAINER_AREA+4, 1, self.text.boundingRect().width(), SETTINGS.CONTAINER_AREA)
        self.text.setX(SETTINGS.CONTAINER_AREA+4)
        self.text.setY(1)


class LeaveContainerButton(ContainerLink):
    def __init__(self, scene_object, view_object):
        super(LeaveContainerButton, self).__init__(scene_object, view_object)

        self.cursor = QtGui.QCursor(QtCore.Qt.UpArrowCursor)
        self.setCursor(self.cursor)

        self.setAcceptHoverEvents(True)

        self.cross()

    def cross(self):
        self.resize()

        cross1 = QtGui.QGraphicsLineItem()
        cross1.setParentItem(self)
        cross1.setLine(self.pos().x()+1, self.pos().y()+2, SETTINGS.CONTAINER_AREA+1, SETTINGS.CONTAINER_AREA+2)
        self.scene_object.addItem(cross1)

        cross2 = QtGui.QGraphicsLineItem()
        cross2.setParentItem(self)
        cross2.setLine(self.pos().x()+1, SETTINGS.CONTAINER_AREA+2, SETTINGS.CONTAINER_AREA+1, 2)
        self.scene_object.addItem(cross2)

    def mouseDoubleClickEvent(self, event):
        self.scene_object.view_object.set_container_scene()

    def resize(self):
        self.adjust_container()

    def adjust_container(self):
        self.setRect(2, 1, SETTINGS.CONTAINER_AREA, SETTINGS.CONTAINER_AREA)


class InputsSourceArea(ContainerLink):
    def __init__(self, scene_object, view_object):
        super(InputsSourceArea, self).__init__(scene_object, view_object)

        self.upstream_nodes = []

        # should be ContainerUI.container_input_channels
        # self.inputs = []

    def adjust_container(self):
        self.setRect(2, SETTINGS.CONTAINER_AREA+3, SETTINGS.CONTAINER_AREA, self.view_object.viewport().height()-5-SETTINGS.CONTAINER_AREA)

        # for output_item in self.outputs:
        #     position = QtCore.QPointF(SETTINGS.CONTAINER_AREA/2,
        #                               (self.outputs.index(output_item)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING))+SETTINGS.OUTPUT_OFFSET)
        #     output_item.setPos(position)

    def add_output(self, output_object=None, port_id=None):
        port = portwidget.Output(node_object=self,
                                 output_object=output_object,
                                 port_id=port_id)
        self.inputs.append(port)
        port.setParentItem(self)
        self.adjust_container()

    def resize(self):
        self.adjust_container()


class OutputsDropArea(ContainerLink):
    def __init__(self, puppeteer, scene_object, view_object):
        super(OutputsDropArea, self).__init__(scene_object, view_object)

        self.puppeteer = puppeteer

        self.setAcceptDrops(True)

        self.connections = []
        self.upstream_connections = []

        # should be ContainerUI.container_output_channels
        # self.container_object.container_output_channels
        # self.outputs = []

        self.setToolTip('drop outputs here to create a container output')

    def adjust_container(self):
        self.setRect(self.view_object.viewport().width()-SETTINGS.CONTAINER_AREA-1, 1, SETTINGS.CONTAINER_AREA, self.view_object.viewport().height()-3)

        for input_item in self.container_object.container_output_channels:
            # if len(self.output)
            position = QtCore.QPointF(self.rect().x() + SETTINGS.CONTAINER_AREA / 2,
                                      (self.container_object.container_output_channels.index(input_item) * (SETTINGS.OUTPUT_RADIUS + SETTINGS.OUTPUT_SPACING)) + SETTINGS.OUTPUT_OFFSET)
            input_item.setPos(position)

    def dragEnterEvent(self, event):
        logging.info('dragEnterEvent on {0}'.format(self))

        if event.mimeData().hasFormat('nodeoutput/draggable-output'):

            data = event.mimeData().data('nodeoutput/draggable-output')
            data = data.data()

            unpickled_output_object = cPickle.loads(data)

            if unpickled_output_object[u'output_graphicsitem_uuid'] in [x.object_id for x in self.container_object.container_output_channels]:
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

    def add_input(self, output_object=None, port_id=None, create_connection=True):

        start_item = self.puppeteer.find_output_graphics_item(scene=self.scene_object, port_id=port_id)
        # start_item = self.scene_object.find_output_graphics_item(port_id=port_id)

        end_item = portwidget.Input(node_object=self,
                                    output_object=output_object,
                                    port_id=port_id,
                                    start_item=start_item)

        self.container_object.container_output_channels.append(end_item)
        end_item.setParentItem(self)

        if create_connection:
            self.add_connection(start_item=start_item, end_item=end_item)

        self.adjust_container()
        self.container_object.update_label()

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

        if event.mimeData().hasFormat('nodeoutput/draggable-output'):
            event.accept()

            data = event.mimeData().data('nodeoutput/draggable-output')
            data = data.data()

            unpickled_output_object = cPickle.loads(data)

            self.add_input(output_object=unpickled_output_object[u'output_object'],
                           port_id=unpickled_output_object[u'output_graphicsitem_uuid'])

        else:
            return QtGui.QGraphicsRectItem.dropEvent(self, event)
