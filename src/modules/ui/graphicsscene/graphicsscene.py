import cPickle
import logging
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import src.modules.ui.nodegraphicsitem.nodegraphicsitem as nodegraphicsitem
import src.conf.settings.SETTINGS as SETTINGS
import src.parser.parse_plugins as parse_plugins
import src.modules.ui.pixmapdraggable.pixmapdraggable as pixmapdraggable


class DraggableMark(QtGui.QGraphicsItem):
    def __init__(self, position, scene):
        super(DraggableMark, self).__init__(None, scene)
        # self.setObjectName( 'fuck' )
        self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemIsMovable)
        # now = datetime.datetime.now()
        # self.setData( 0, 'Das ist mein Name' )
        # self.setData( 1, 'fuck' )
        # self.rect = QtCore.QRectF(position.x(), position.y(), 15, 15)
        self.rect = QtCore.QRectF(-30, -30, 120, 60)
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
            print 'hallo'
            # print dir( self.data( 0 ) )
            # print self.data( 0 )..toString
            # print self.data( 0 ).type
        painter.setPen(pen)
        # brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        # painter.setBrush(brush)
        painter.setBrush(QtGui.QColor(200, 0, 0))
        # painter.drawEllipse(self.rect)
        painter.drawRoundedRect(self.rect, 10.0, 10.0)
        # painter.drawLine(20, 160, 250, 160)


class GraphicsScene(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)

        self.graphicsview = parent

        self.base_rect = self.addRect(QtCore.QRectF(0, 0, 500, 500), QtGui.QColor(255, 0, 0, 0))

        self.global_scale = 1

        self.node_items = []

        self.item_group = QtGui.QGraphicsItemGroup()

        # item1 = QtGui.QGraphicsRectItem(0, 0, 100, 100)
        # item1.setBrush(QtGui.QBrush(QtCore.Qt.red))
        # item1.setAcceptDrops(True)
        # item1.setFlags(item1.ItemIsSelectable | item1.ItemIsMovable)
        # self.addItem(item1)
        # print item1.zValue()
        # print item1.acceptDrops()

        # plugins = parse_plugins.get_plugins()

        # plugins = parse_plugins.get_plugins()

        # attributes = dir(plugins[0])
        # for attribute in attributes:
        #     print '%s = %s' % (attribute, getattr(plugins[1], attribute))

        # plugin = pixmapdraggable.PixmapFullFeature(plugin=plugins[0], mainwindow=None)
        #
        # node = nodegraphicsitem.NodeGraphicsItem(position=QtCore.QPoint(100, 100), plugin=plugin)
        # self.addItem(node)

    def dragEnterEvent(self, event):
        # event.accept()
        if event.mimeData().hasFormat('node/draggable-pixmap'):
            # print 'and here (canvas)', event
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

            node_graphics_item = nodegraphicsitem.NodeGraphicsItem(position=pos, plugin=unpickled_plugin_object)
            # print unpickled_plugin_object
            if SETTINGS.NODE_CREATE_COLLAPSED:
                node_graphics_item.expand_layout()
            node_graphics_item.setScale(self.global_scale)
            self.addItem(node_graphics_item)
            node_graphics_item.setParentItem(self.base_rect)
            self.node_items.append(node_graphics_item)

            # node_group = nodegraphicsitem.NodeGroup(position=pos, plugin=unpickled_plugin_object)
            # self.addItem(node_group)
            # node_group.setParentItem(self.base_rect)
            # node_group.setParentItem(self.base_rect)
            # self.node_items.append(node_group)

            # self.graphicsview.setAcceptDrops(False)

            # rect = self.itemsBoundingRect()
            # rect.adjust(-20, -20, 20, 20)
            #
            # self.setSceneRect(rect)
            #
            # rect = self.addRect(QtCore.QRectF(pos.x(), pos.y(), 20, 20), QtCore.Qt.red)

            # painter.setBackgroundMode( Qt::OpaqueMode );
            # painter.setBackground( QColor( Qt::gray ) );
            # painter.setPen( QPen( Qt::black ) );
            # painter.setBrush( QBrush( Qt::black, Qt::BDiagPattern ) );

            # unPickleData = userListModule.ListBaseClass.d[unPickleData]
            # Create the node in the scene
            # self.createNode(unPickleData, event.scenePos())
            # if unPickleData.dictKey is 'emitterCat':
            #
            #     newPos = event.scenePos()
            #     newPos.setY(newPos.y()-175)
            #     # behaviorNode = mayaNodesModule.MayaNodes['behaviorCat']
            #     # self.createNode(behaviorNode, newPos)

        else:
            return QtGui.QGraphicsScene.dropEvent(self, event)

    def dragMoveEvent(self, event):
        logging.info('dragMoveEvent on {0}'.format(self))
        if event.mimeData().hasFormat('node/draggable-pixmap'):
            event.accept()
            logging.info('mimeData of event {0} data has format node/draggable-pixmap'.format(event))
        else:
            return QtGui.QGraphicsScene.dragMoveEvent(self, event)
