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
        # pseudo code:
        # - group nodes (or maybe use childrenBoundingRect())
        # - set the pivot of the group to mouse cursor point
        # - do the transformation (scaling)
        # - ungroup but keep the transformation (scaling and position)

        # absolute pos of mouse cursor in scene
        event_pos = self.mapToScene(event.pos())

        factor = 1.2

        # point = QtGui.QGraphicsRectItem(event_pos.x()-10, event_pos.y()-10, 20, 20)

        self.point.setPos(event_pos)
        # print event_pos

        # self.scene.addItem(point)

        # point.set

        # print dir(self.scene.random_item)
        # print dir(self.scene.random_rect)

        # prev_parent = self.scene.random_item.parentItem()

        # self.scene.item_group.setOffset(event_pos)

        # group_pos = self.mapFromScene(self.scene.item_group.pos())

        # self.scene.item_group.setParentItem(self.point)

        self.scene.item_group.setTransformOriginPoint(event_pos)
        # self.scene.item_group.setTransformOriginPoint(event.pos())


        if event.delta() > 0:
            # self.scene.random_item.setPos(event.pos())
            # self.scene.base_rect.setScale(self.scene.base_rect.scale() * factor)

            # self.scene.random_item.setScale(self.scene.random_item.scale() * factor)

            # group_pos = self.scene.item_group.pos()

            self.point.setScale(self.point.scale() * factor)

            # group_pos = self.mapFromScene(self.scene.item_group.pos())

            # new_group_pos = self.mapFromScene(self.scene.item_group.pos())

            # self.scene.item_group.setPos(group_pos * 20)


            # self.scene.random_item.setPos(event_pos)
            # for item in self.items():
            #     print dir(item)
            #     item.setScale(item.scale()*factor)
        else:
            # self.scene.random_item.setPos(event.pos())
            # self.scene.base_rect.setScale(self.scene.base_rect.scale() / factor)

            # self.scene.random_item.setScale(self.scene.random_item.scale() / factor)
            self.point.setScale(self.point.scale() / factor)

            # self.scene.random_item.setPos(event_pos)
            # for item in self.items():
            #     print dir(item)
            #     item.setScale(item.scale()/factor)

        print self.point.pos()

        # new_group_pos = self.mapFromScene(self.scene.item_group.pos())

        # print self.map

        # print self.mapFromScene(self.scene.item_group.pos())
        # print self.mapToScene(int(self.scene.item_group.pos().x()), int(self.scene.item_group.pos().y()))
        # print self.mapToGlobal(QtCore.QPoint(int(self.scene.item_group.pos().x()), int(self.scene.item_group.pos().y())))
        # print self.mapFromGlobal(QtCore.QPoint(int(self.scene.item_group.pos().x()), int(self.scene.item_group.pos().y())))
        #
        # print self.mapFrom(self.scene.item_group, QtCore.QPoint(int(self.scene.item_group.pos().x()), int(self.scene.item_group.pos().y())))
        scale = self.point.scale()

        # print self.scene.random_item.scale()
        # self.scene.random_item.setParentItem(prev_parent)
        # self.scene.item_group.setParentItem(prev_parent)
        # self.scene.item_group.setPos(self.mapToScene(new_group_pos))


        self.scene.item_group.setScale(scale)
        # self.mapToParent(self.scene.item_group, event_pos)

        # print group_pos.x()

        # print self.scene.random_item.scale()
        # self.scene.removeItem(point)

    def move(self, event):
        # absolute pos of mouse cursor in scene
        event_pos = self.mapToScene(event.pos())

        rect_center = QtCore.QPoint((self.scene.random_rect.width()-self.scene.random_rect.x())/2, (self.scene.random_rect.height()-self.scene.random_rect.y())/2)

        print rect_center
        # print self.mapToScene(rect_center)


    def wheelEvent(self, event):

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
