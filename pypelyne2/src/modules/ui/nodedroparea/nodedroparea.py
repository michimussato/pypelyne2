import uuid
import cPickle
import logging
import PyQt4.QtGui as QtGui


class NodeDropArea(QtGui.QGraphicsRectItem):
    def __init__(self, puppeteer, node_object):
        super(NodeDropArea, self).__init__()

        self.puppeteer = puppeteer

        self.node = node_object

        # self.allowed = True

        self.pen = QtGui.QPen(QtGui.QColor(0, 0, 0, 0))
        self.setPen(self.pen)

        self.brush = QtGui.QBrush()
        self.setBrush(self.brush)

        self.brush_active = QtGui.QColor(0, 255, 0, 100)
        self.brush_forbidden = QtGui.QColor(255, 0, 0, 100)
        self.brush_inactive = QtGui.QColor(255, 0, 0, 0)

        # self.drop_area = nodedroparea.NodeDropArea(self)

        self.setZValue(self.node.zValue() + 1)
        self.setParentItem(self.node)

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

        logging.info('dragEnterEvent on NodeDropArea ({0})'.format(self))
        if event.mimeData().hasFormat('output/draggable-pixmap'):
            self.set_active()
            logging.info('mimeData of event {0} data has format output/draggable-pixmap'.format(event))

        elif event.mimeData().hasFormat('nodeoutput/draggable-output'):

            data = event.mimeData().data('nodeoutput/draggable-output')
            data = data.data()

            unpickled_output_object = cPickle.loads(data)

            if unpickled_output_object[u'output_graphicsitem_uuid'] in [x.object_id for x in self.node.inputs]:
                logging.warning('output with uuid {0} {1} is already connected to {2}'.format(unpickled_output_object[u'output_graphicsitem_uuid'],
                                                                                              unpickled_output_object[u'output_object'],
                                                                                              self.node))
                self.set_forbidden()

            elif self.node.hovered:
                self.set_forbidden()
            else:
                self.set_active()

        return QtGui.QGraphicsRectItem.dragEnterEvent(self, event)

    def dragLeaveEvent(self, event):
        logging.info('dragLeaveEvent on NodeDropArea ({0})'.format(self))
        self.set_inactive()
        # self.setAcceptDrops(True)

    def dragMoveEvent(self, event):
        logging.info('dragMoveEvent on NodeDropArea ({0})'.format(self))
        # self.setAcceptDrops(False)

    def dropEvent(self, event):
        logging.info('dropEvent on NodeDropArea ({0})'.format(self))
        self.set_inactive()

        if event.mimeData().hasFormat('output/draggable-pixmap'):
            event.accept()

            data = event.mimeData().data('output/draggable-pixmap')
            data = data.data()

            unpickled_output_object = cPickle.loads(data)

            logging.info('mimeData of event {0} data has format output/draggable-pixmap'.format(event))
            logging.info('{0}/{1} --> {2}'.format(unpickled_output_object.output,
                                                  unpickled_output_object.abbreviation,
                                                  self.node))

            new_output = self.puppeteer.create_output(node=self.node,
                                                      output_object=unpickled_output_object)

        elif event.mimeData().hasFormat('nodeoutput/draggable-output'):
            event.accept()

            data = event.mimeData().data('nodeoutput/draggable-output')
            data = data.data()

            unpickled_output_object = cPickle.loads(data)

            # start_item = self.puppeteer.find_output_graphics_item(scene=self.scene(),
            #                                                       port_id=unpickled_output_object[u'output_graphicsitem_uuid'])

            new_input = self.puppeteer.create_input(scene=self.scene(),
                                                    node=self.node,
                                                    output_object=unpickled_output_object[u'output_object'],
                                                    start_port_id=unpickled_output_object[u'output_graphicsitem_uuid'])

            if new_input != 0:

                new_connection = self.puppeteer.add_connection(scene=self.scene(),
                                                               start_port_id=unpickled_output_object[u'output_graphicsitem_uuid'],
                                                               end_item=new_input)

        else:
            return QtGui.QGraphicsRectItem.dropEvent(self, event)
