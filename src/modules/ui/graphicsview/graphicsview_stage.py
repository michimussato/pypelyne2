import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import src.modules.ui.graphicsview.graphicsview as graphicsview
import src.modules.ui.graphicsscene.graphicsscene as graphicsscene
# import src.modules.ui.rectangle.rectangle as rectangle


class GraphicsViewStage(graphicsview.GraphicsView):
    def __init__(self):
        super(GraphicsViewStage, self).__init__()
        self.scene = graphicsscene.GraphicsScene()
        self.setScene(self.scene)

        self.point = QtGui.QGraphicsRectItem(-10, -10, 20, 20)
        self.scene.addItem(self.point)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        # self.scene.random_item.setParentItem(self.point)

        # self.setResizeAnchor(self.AnchorUnderMouse)
        # self.setTransformationAnchor(self.AnchorUnderMouse)

        # self.setResizeAnchor(self.AnchorUnderMouse)
        # self.setSceneRect(0, 0, 500, 500)

        # self.resize(self.scene.width(), self.scene.height())
        # self.setCentralWidget(self.view)
        # self.setAcceptDrops(True)
        # self.rectangle = rectangle.Rectangle()
        # self.scene.addItem(self.rectangle)

    def scale(self, event):
        # print type(self.scene.node_items)
        group = self.scene.createItemGroup(self.scene.node_items)

        # absolute pos of mouse cursor in scene
        event_pos_scene = self.mapToScene(event.pos())

        increment = 0.1

        self.point.setPos(event_pos_scene)

        group.setTransformOriginPoint(event_pos_scene)

        if event.delta() > 0:
            self.point.setScale(self.point.scale() + increment)
            group.setScale(group.scale() + increment)
        else:
            self.point.setScale(self.point.scale() - increment)
            group.setScale(group.scale() - increment)

        self.scene.destroyItemGroup(group)

        # print self.scene.node_items[0].scale()

    def move(self, event):
        # absolute pos of mouse cursor in scene
        event_pos = self.mapToScene(event.pos())

        rect_center = QtCore.QPoint((self.scene.random_rect.width()-self.scene.random_rect.x())/2, (self.scene.random_rect.height()-self.scene.random_rect.y())/2)

        print rect_center
        # print self.mapToScene(rect_center)


    def wheelEvent(self, event):

        # print 'asdf', self.scene.item_group.pos()

        self.scale(event)
        # self.move(event)

        # # print dir(self.rect.setRect())
        # factor = 1.2
        # # print dir(event)
        # print event.pos()
        # event_pos = event.pos()
        # map_to_scene = self.mapToScene(event_pos)
        # map_to_base_rect = self.scene.base_rect.mapFromItem(self.scene.base_rect, event_pos)
        #
        # point = QtCore.QPointF(event_pos)
        # print point
        #
        # print self.mapToScene(event.pos())
        # # print dir(self)
        # # print self.mapFromScene(self.scene.base_rect, event.pos())
        # if event.delta() > 0:
        #     # self.scene.random_item.setPos(event.pos())
        #     # self.scene.base_rect.setScale(self.scene.base_rect.scale() * factor)
        #     self.scene.random_item.setScale(self.scene.random_item.scale() * factor)
        #     self.scene.random_item.setPos(map_to_base_rect)
        #     # for item in self.items():
        #     #     print dir(item)
        #     #     item.setScale(item.scale()*factor)
        # else:
        #     # self.scene.random_item.setPos(event.pos())
        #     # self.scene.base_rect.setScale(self.scene.base_rect.scale() / factor)
        #     self.scene.random_item.setScale(self.scene.random_item.scale() / factor)
        #     self.scene.random_item.setPos(map_to_base_rect)
        #     # for item in self.items():
        #     #     print dir(item)
        #     #     item.setScale(item.scale()/factor)

    def resizeEvent(self, event):
        # print dir(self)
        # print event

        self.setSceneRect(0, 0, self.width(), self.height())
        # print self.graphicssview_stage.sceneRect().width()
        # print self.graphicssview_stage.sceneRect().height()

        # print self.rect()

        # self.graphicssview_stage.scene.setSceneRect(self.graphicssview_stage.rect())
        self.scene.base_rect.setRect(QtCore.QRectF(self.rect()))

    # def wheelEvent(self, event):
    #     print 'hi'
    #     sc = event.delta()/100000
    #     if sc < 0:
    #         sc -= 1/sc
    #     self.scale(sc, sc)
        # self.setDragMode(0)
        # self.scene.showMatrix()


        # # numSteps = event.delta() / 15 / 8
        # #
        # # if numSteps == 0:
        # #     event.ignore()
        # #
        # # sc = 1.25 * numSteps
        # # self.zoom(sc, self.mapToScene(event.pos()))
        # # event.accept()
        #
        # # delta = 2 * (event.pos().x())
        # # self.setResizeAnchor(self.AnchorViewCenter)
        #
        # factor = event.delta()/1000
        #
        # # print self.visibleRegion().boundingRect()
        #
        # # for i in dir(self):
        # #     if not i.startswith('_'):
        # #         print i, getattr(self, i)
        #
        # # print self.x()
        # # print self.y()
        # # print event.pos()
        # # print self.frameRect()
        # # print self.frameSize()
        #
        # print ''
        # visible_rect = self.mapToScene(self.rect()).boundingRect()
        # self.setSceneRect(visible_rect)
        # print self.sceneRect()
        # print visible_rect
        # # print self.mapFromScene(self.mapToScene(self.rect()).boundingRect()).boundingRect()
        # print self.mapToScene(event.pos())
        #
        # self.scale(factor, factor)
        #
        # # #self.nodeView.centerOn()
        # #
        # # #print 'event.delta() = %s' %event.delta()
        # #
        # # if event.delta() > 0:
        # #     self.scale(factor, factor)
        # #     # self.centerOn()
        # #     # self.centerOn(self.mapToScene(event.pos()))
        # #
        # # else:
        # #     self.scale(1.0 / factor, 1.0 / factor)
        # #     # self.centerOn(self.mapToScene(event.pos()))
        # #
        # # # self.setResizeAnchor(self.AnchorUnderMouse)
