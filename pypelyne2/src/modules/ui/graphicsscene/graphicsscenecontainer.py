import cPickle
import logging
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.modules.ui.containerui.containerui as containerui
import pypelyne2.src.modules.ui.navigator.navigator as navigator
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class GraphicsSceneContainer(QtGui.QGraphicsScene):
    def __init__(self, view_object=None):
        super(GraphicsSceneContainer, self).__init__(view_object)

        self.view_object = view_object

        self.base_rect = self.addRect(QtCore.QRectF(), QtGui.QColor(255, 0, 0, 0))

        self.point = QtGui.QGraphicsRectItem(-10, -10, 20, 20)
        if SETTINGS.DISPLAY_TRANSFORM_ANCHOR:
            self.addItem(self.point)

        self.global_scale = 1

        self.node_items = []
        self.connection_items = []

        self.navigator = navigator.Navigator(scene_object=self,
                                             view_object=self.view_object)

        # self.container_items = []

        self.item_group = QtGui.QGraphicsItemGroup()

    def dragEnterEvent(self, event):
        # event.accept()
        if event.mimeData().hasFormat('container/draggable-pixmap'):
            logging.info('dragEnterEvent accepted')
            event.accept()
        # if event.mimeData().hasFormat('node/draggable-pixmap'):
        #     logging.info('dragEnterEvent accepted')
        #     event.accept()
        else:
            return QtGui.QGraphicsScene.dragEnterEvent(self, event)

    def dropEvent(self, event):
        logging.info('something was dropped onto {0}'.format(self))
        if event.mimeData().hasFormat('container/draggable-pixmap'):
            event.accept()

            pos = event.scenePos()
            data = event.mimeData().data('container/draggable-pixmap')
            data = data.data()

            unpickled_container_object = cPickle.loads(data)

            logging.info('{0} dropped onto canvas (drop event accepted)'.format(unpickled_container_object))

            container_item = containerui.ContainerUI(position=pos, container=unpickled_container_object, scene_object=self)

            container_item.setScale(self.global_scale)
            self.addItem(container_item)
            self.node_items.append(container_item)
            self.addItem(container_item)

        else:
            return QtGui.QGraphicsScene.dropEvent(self, event)

    def dragMoveEvent(self, event):
        logging.info('dragMoveEvent on {0}'.format(self))
        if event.mimeData().hasFormat('container/draggable-pixmap'):
            event.accept()
            logging.info('mimeData of event {0} data has format container/draggable-pixmap'.format(event))
        else:
            return QtGui.QGraphicsScene.dragMoveEvent(self, event)

    def find_output_graphics_item(self, port_id):
        for node_item in self.node_items:
            for output_graphics_item in node_item.outputs:
                if output_graphics_item.uuid == port_id:
                    return output_graphics_item

    def expand_container(self, container_item):
        # print self.node_items
        self.hide_containers()

    def hide_containers(self):
        for container in self.node_items:
            container.setVisible(False)