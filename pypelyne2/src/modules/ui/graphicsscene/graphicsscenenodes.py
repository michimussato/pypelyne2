import cPickle
import logging
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.modules.ui.navigator.navigator as navigator
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.modules.ui.containerlink.containerlink as containerlink


class GraphicsSceneNodes(QtGui.QGraphicsScene):
    def __init__(self, puppeteer, view_object=None, container_object=None):
        super(GraphicsSceneNodes, self).__init__(view_object)

        self.puppeteer = puppeteer

        self.view_object = view_object

        self.container_object = container_object

        self.base_rect = self.addRect(QtCore.QRectF(), QtGui.QColor(255, 0, 0, 0))

        self.point = QtGui.QGraphicsRectItem(-10, -10, 20, 20)
        if SETTINGS.DISPLAY_TRANSFORM_ANCHOR:
            self.addItem(self.point)

        self.global_scale = 1

        self.node_items = []
        self.connection_items = []

        self.navigator = navigator.Navigator(scene_object=self,
                                             view_object=self.view_object)

        self.leave_container_button = containerlink.LeaveContainerButton(scene_object=self,
                                                                         view_object=self.view_object)
        self.output_area = containerlink.OutputsDropArea(puppeteer=self.puppeteer,
                                                         scene_object=self,
                                                         view_object=self.view_object)
        self.input_area = containerlink.InputsSourceArea(scene_object=self,
                                                         view_object=self.view_object)
        self.label_area = containerlink.ContainerLabel(scene_object=self,
                                                       view_object=self.view_object)

        self.item_group = QtGui.QGraphicsItemGroup()

    def dragEnterEvent(self, event):
        # event.accept()
        if event.mimeData().hasFormat('node/draggable-pixmap'):
            logging.info('dragEnterEvent accepted')
            event.accept()
        else:
            return QtGui.QGraphicsScene.dragEnterEvent(self, event)

    def dropEvent(self, event):
        logging.info('something was dropped onto {0}'.format(self))

        if event.mimeData().hasFormat('node/draggable-pixmap'):
            event.accept()

            pos = event.scenePos()
            data = event.mimeData().data('node/draggable-pixmap')
            data = data.data()

            unpickled_plugin_object = cPickle.loads(data)

            logging.info('{0} dropped onto canvas (drop event accepted)'.format(unpickled_plugin_object))

            self.puppeteer.create_node(scene=self,
                                       plugin_object=unpickled_plugin_object,
                                       position=pos)

            # self.create_node(position=pos, plugin=unpickled_plugin_object)

            # node_graphics_item = nodeui.NodeUI(position=pos, plugin=unpickled_plugin_object, scene_object=self)
            # if SETTINGS.NODE_CREATE_COLLAPSED:
            #     node_graphics_item.expand_layout()
            # node_graphics_item.setScale(self.global_scale)
            # self.addItem(node_graphics_item)
            # node_graphics_item.setParentItem(self.base_rect)
            # self.node_items.append(node_graphics_item)

        else:
            return QtGui.QGraphicsScene.dropEvent(self, event)

    def dragMoveEvent(self, event):
        logging.info('dragMoveEvent on {0}'.format(self))
        if event.mimeData().hasFormat('node/draggable-pixmap'):
            event.accept()
            logging.info('mimeData of event {0} data has format node/draggable-pixmap'.format(event))
        else:
            return QtGui.QGraphicsScene.dragMoveEvent(self, event)

    # def find_output_graphics_item(self, port_id):
    #     for node_item in self.node_items:
    #         for output_graphics_item in node_item.outputs:
    #             if output_graphics_item.object_id == port_id:
    #                 return output_graphics_item
