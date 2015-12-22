import cPickle
from PyQt4 import QtGui
from PyQt4 import QtCore
import src.modules.ui.nodegraphicsitem.nodegraphicsitem as nodegraphicsitem


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

        # self.base_rect_color = QtGui.QColor(255, 0, 0)

        self.base_rect = self.addRect(QtCore.QRectF(0, 0, 500, 500), QtGui.QColor(255, 0, 0, 0))

        # self.installEventFilter(self)

        # self.item_group = QtGui.QGraphicsItemGroup()

        self.global_scale = 1

        self.node_items = []


        # self.test_rect = self.addRect(QtCore.QRectF(400, 100, 40, 40), QtCore.Qt.green)
        # self.node_items.append(self.test_rect)
        #
        # for i in range(20):
        #     rect = self.addRect(QtCore.QRectF(i*20, i*20, 40, 40))
        #     self.node_items.append(rect)

        self.item_group = QtGui.QGraphicsItemGroup()

        # self.addItem(self.item_group)

    # def eventFilter(self, source, event):
    #     if event.type() == QtCore.QEvent.MouseMove:
    #         pos = event.pos()
    #         print('mouse move: (%d, %d)' % (pos.x(), pos.y()))
    #     return QtGui.QWidget.eventFilter(self, source, event)

    def dragEnterEvent(self, event):
        # event.accept()
        print 'and here', event

    def dropEvent(self, event):
        print 'here'
        # print dir(event.mimeData())
        if event.mimeData().hasFormat('node/draggable-pixmap'):
            event.accept()
            pos = event.scenePos()
            print 'accepted'
            data = event.mimeData().data('node/draggable-pixmap')
            data = data.data()

            unpickled_plugin_object = cPickle.loads(data)

            # print dir(unpickled_plugin_object)

            # print unPickleData.dictKey
            # TODO: map to self.rect
            node_graphics_item = nodegraphicsitem.NodeGraphicsItem(position=pos, plugin=unpickled_plugin_object)
            node_graphics_item.setScale(self.global_scale)
            self.addItem(node_graphics_item)
            # nodegraphicsitem.installSceneEventFilter(nodegraphicsitem)

            node_graphics_item.setParentItem(self.base_rect)

            self.node_items.append(node_graphics_item)

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

    def dragMoveEvent(self, event):
        print 'there'
        if event.mimeData().hasFormat("application/x-imgname"):
            event.accept()
