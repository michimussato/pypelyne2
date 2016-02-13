import uuid
import cPickle
import logging
import PyQt4.QtGui as QtGui


class ContainerDropArea(QtGui.QGraphicsRectItem):
    def __init__(self, puppeteer, container_object):
        super(ContainerDropArea, self).__init__()

        self.puppeteer = puppeteer

        self.container = container_object

        # self.allowed = True

        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
        self.setPen(self.pen)

        self.brush = QtGui.QBrush()
        self.setBrush(self.brush)

        self.brush_active = QtGui.QColor(0, 255, 0, 100)
        self.brush_forbidden = QtGui.QColor(255, 0, 0, 100)
        self.brush_inactive = QtGui.QColor(255, 0, 0, 0)

        self.setZValue(self.container.zValue() + 1)
        self.setParentItem(self.container)

        self.setAcceptDrops(True)

        self.set_inactive()

    def set_active(self):
        self.setBrush(self.brush_active)
        logging.info('setting drop area active on {0}'.format(self))

    def set_forbidden(self):
        self.setBrush(self.brush_forbidden)
        logging.info('setting drop area forbidden on {0}'.format(self))

    def set_inactive(self):
        self.setBrush(self.brush_inactive)
        logging.info('setting drop area inactive on {0}'.format(self))

    def dragEnterEvent(self, event):

        logging.info('dragEnterEvent on ContainerDropArea ({0})'.format(self))
        # if event.mimeData().hasFormat('output/draggable-pixmap'):
        #     self.set_active()
        #     logging.info('mimeData of event {0} data has format output/draggable-pixmap'.format(event))

        if event.mimeData().hasFormat('containeroutput/draggable-output'):

            data = event.mimeData().data('containeroutput/draggable-output')
            data = data.data()

            unpickled_output_object = cPickle.loads(data)

            # if unpickled_output_object[u'output_graphicsitem_uuid'] in [x.object_id for x in self.container.inputs]:
            if False:
                logging.warning('output with uuid {0} {1} is already connected to {2}'.format(unpickled_output_object[u'output_graphicsitem_uuid'],
                                                                                              unpickled_output_object[u'output_object'],
                                                                                              self.container))
                self.set_forbidden()

            elif self.container.hovered:
                self.set_forbidden()
            else:
                self.set_active()

        else:
            self.set_forbidden()

        return QtGui.QGraphicsRectItem.dragEnterEvent(self, event)

    def dragLeaveEvent(self, event):
        logging.info('dragLeaveEvent on ContainerDropArea ({0})'.format(self))
        self.set_inactive()
        # self.setAcceptDrops(True)

    def dragMoveEvent(self, event):
        logging.info('dragMoveEvent on ContainerDropArea ({0})'.format(self))
        # self.setAcceptDrops(False)

    def dropEvent(self, event):
        logging.info('dropEvent on ContainerDropArea ({0})'.format(self))
        self.set_inactive()

        # if event.mimeData().hasFormat('output/draggable-pixmap'):
        #     event.accept()
        #
        #     data = event.mimeData().data('output/draggable-pixmap')
        #     data = data.data()
        #
        #     unpickled_output_object = cPickle.loads(data)
        #
        #     logging.info('mimeData of event {0} data has format output/draggable-pixmap'.format(event))
        #     logging.info('{0}/{1} --> {2}'.format(unpickled_output_object.output,
        #                                           unpickled_output_object.abbreviation,
        #                                           self.container))
        #     self.container.add_output(output_object=unpickled_output_object,
        #                               port_id=str(uuid.uuid4()))

        if event.mimeData().hasFormat('containeroutput/draggable-output'):
            event.accept()

            data = event.mimeData().data('containeroutput/draggable-output')
            data = data.data()

            unpickled_output_object = cPickle.loads(data)

            print unpickled_output_object[u'output_graphicsitem_uuid']
            print self.container.output_port.object_id
            print dir(unpickled_output_object)

            # self.scene

            self.puppeteer.add_input_container(scene=self.container.scene_object,
                                               port_id=unpickled_output_object[u'output_graphicsitem_uuid'],
                                               end_item=self.container.input_port)

        else:
            return QtGui.QGraphicsRectItem.dropEvent(self, event)
