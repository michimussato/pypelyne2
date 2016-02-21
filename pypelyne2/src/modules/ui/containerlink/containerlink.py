import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import logging
import cPickle
# import pypelyne2.src.modules.ui.portwidget.portwidget as portwidget
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


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
        self.arrange_outputs()
        self.arrange_inputs()
        self.container_object.update_label()
        # self.adjust_container()


class ContainerLabel(ContainerLink):
    def __init__(self, scene_object, view_object):
        super(ContainerLabel, self).__init__(scene_object, view_object)

        self.text = QtGui.QGraphicsTextItem()
        self.text.setParentItem(self)
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

        # self.upstream_nodes = []

        self.outputs = []

        # should be ContainerUI.container_input_channels
        # self.inputs = []

    def adjust_container(self):
        self.setRect(2, SETTINGS.CONTAINER_AREA+3, SETTINGS.CONTAINER_AREA, self.view_object.viewport().height()-5-SETTINGS.CONTAINER_AREA)

        # for output_item in self.outputs:
        #     position = QtCore.QPointF(SETTINGS.CONTAINER_AREA/2,
        #                               (self.outputs.index(output_item)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING))+SETTINGS.OUTPUT_OFFSET)
        #     output_item.setPos(position)

    # def add_output(self, port):
    #
    #     print 'heeeee'
    #     # port = portwidget.Output(node_object=self,
    #     #                          output_object=output_object,
    #     #                          port_id=port_id)
    #
    #     self.outputs.append(port)
    #     # port.setParentItem(self)
    #
    #     # self.scene_object.addItem(port)
    #
    #     self.arrange_outputs()
    #
    #     self.adjust_container()

    def arrange_outputs(self):
        self.setRect(SETTINGS.CONTAINER_AREA/2,
                     1,
                     SETTINGS.CONTAINER_AREA,
                     self.view_object.viewport().height()-3)

        for output_item in self.outputs:

            # print dir(input_item)

            position = QtCore.QPointF(self.rect().x()+SETTINGS.CONTAINER_AREA/2,
                                      (self.outputs.index(output_item)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING))+SETTINGS.OUTPUT_OFFSET)

            output_item.setPos(position)

    def arrange_inputs(self):
        pass

    # def resize(self):
    #     self.adjust_container()


class OutputsDropArea(ContainerLink):
    def __init__(self, puppeteer, scene_object, view_object):
        super(OutputsDropArea, self).__init__(scene_object, view_object)

        self.puppeteer = puppeteer

        self.setAcceptDrops(True)

        # this is actually the output bar
        self.inputs = []

        # self.connections = []
        # self.upstream_connections = []

        # should be ContainerUI.container_output_channels
        # self.container_object.container_output_channels
        # self.outputs = []

        self.setToolTip('drop outputs here to create a container output')

    def arrange_outputs(self):
        pass

    def arrange_inputs(self):
        self.setRect(self.view_object.viewport().width()-SETTINGS.CONTAINER_AREA-1,
                     1,
                     SETTINGS.CONTAINER_AREA,
                     self.view_object.viewport().height()-3)

        for input_item in self.inputs:

            # print dir(input_item)

            position = QtCore.QPointF(self.rect().x()+SETTINGS.CONTAINER_AREA/2,
                                      (self.inputs.index(input_item)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING))+SETTINGS.OUTPUT_OFFSET)

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

    def dropEvent(self, event):
        logging.info('dropEvent on {0}'.format(self))

        if event.mimeData().hasFormat('nodeoutput/draggable-output'):
            event.accept()

            data = event.mimeData().data('nodeoutput/draggable-output')
            data = data.data()

            unpickled_output_object = cPickle.loads(data)

            new_input = self.puppeteer.create_asset_output(scene=self.scene_object,
                                                           node=self,
                                                           output_object=unpickled_output_object[u'output_object'],
                                                           start_port_id=unpickled_output_object[u'output_graphicsitem_uuid'],
                                                           container_object=self.container_object)

            if new_input != 0:

                new_connection = self.puppeteer.add_connection(scene=self.scene_object,
                                                               start_port_id=unpickled_output_object[u'output_graphicsitem_uuid'],
                                                               end_item=new_input)

        else:
            return QtGui.QGraphicsRectItem.dropEvent(self, event)
