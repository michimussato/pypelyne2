import cPickle
import logging
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.modules.ui.nodegraphicsitem.nodegraphicsitem as nodegraphicsitem
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
# import pypelyne2.src.parser.parse_plugins as parse_plugins
# import pypelyne2.src.modules.ui.pixmapdraggable.pixmapdraggable as pixmapdraggable


class DraggableMark(QtGui.QGraphicsItem):
    def __init__(self, position, scene):
        super(DraggableMark, self).__init__(None, scene)
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemIsMovable)

        self.rect = QtCore.QRectF()
        self.setPos(position)
        scene.clearSelection()

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(3)

        if option.state & QtGui.QStyle.State_Selected:
            pen.setColor(QtCore.Qt.green)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(200, 0, 0))
        painter.drawRoundedRect(self.rect, 10.0, 10.0)


class GraphicsScene(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)

        self.graphicsview = parent

        self.base_rect = self.addRect(QtCore.QRectF(0, 0, 500, 500), QtGui.QColor(255, 0, 0, 0))

        self.global_scale = 1

        self.node_items = []

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

            node_graphics_item = nodegraphicsitem.NodeGraphicsItem(position=pos, plugin=unpickled_plugin_object, scene=self)
            if SETTINGS.NODE_CREATE_COLLAPSED:
                node_graphics_item.expand_layout()
            node_graphics_item.setScale(self.global_scale)
            self.addItem(node_graphics_item)
            node_graphics_item.setParentItem(self.base_rect)
            self.node_items.append(node_graphics_item)

        else:
            return QtGui.QGraphicsScene.dropEvent(self, event)

    def dragMoveEvent(self, event):
        logging.info('dragMoveEvent on {0}'.format(self))
        if event.mimeData().hasFormat('node/draggable-pixmap'):
            event.accept()
            logging.info('mimeData of event {0} data has format node/draggable-pixmap'.format(event))
        else:
            return QtGui.QGraphicsScene.dragMoveEvent(self, event)
