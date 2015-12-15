import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import src.modules.ui.graphicsview.graphicsview as graphicsview
import src.modules.ui.graphicsscene.graphicsscene as graphicsscene
import src.conf.settings.SETTINGS as SETTINGS
# import src.modules.ui.rectangle.rectangle as rectangle


class GraphicsViewStage(graphicsview.GraphicsView):
    def __init__(self):
        super(GraphicsViewStage, self).__init__()
        self.scene = graphicsscene.GraphicsScene()
        self.setScene(self.scene)

        self.setMouseTracking(False)

        self.point = QtGui.QGraphicsRectItem(-10, -10, 20, 20)
        self.scene.addItem(self.point)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    # def mousePressEvent(self, event):
    #     pass
    #
    # def keyPressEvent(self, event):
    #     modifiers = QtGui.QApplication.keyboardModifiers()
    #     if modifiers == QtCore.Qt.AltModifier:
    #         self.setDragMode(self.ScrollHandDrag)
    #
    # def keyReleaseEvent(self, event):
    #     self.setDragMode(self.RubberBandDrag)
    #
    #
    # def mouseMoveEvent(self, event):
    #     # dragMode 1: scrollhanddrag
    #     # dragmode 2: rubberbanddrag
    #     if self.dragMode() == 1:
    #         # print self.dragMode()
    #         group = self.scene.createItemGroup(self.scene.node_items)
    #         event_pos_scene = self.mapToScene(event.pos())
    #
    #         # print event_pos_scene
    #
    #         print dir(self.scene.test_rect)
    #
    #         # self.scene.test_rect.translate(event_pos_scene)
    #         group.setPos(event_pos_scene)
    #
    #         # print 'moving'
    #
    #         self.scene.destroyItemGroup(group)

    def wheelEvent(self, event):
        # print 'scaling'
        # print type(self.scene.node_items)
        group = self.scene.createItemGroup(self.scene.node_items)

        # absolute pos of mouse cursor in scene
        event_pos_scene = self.mapToScene(event.pos())

        self.point.setPos(event_pos_scene)

        group.setTransformOriginPoint(event_pos_scene)

        if event.delta() > 0:
            self.point.setScale(self.point.scale() * (1+SETTINGS.ZOOM_INCREMENT))
            group.setScale(group.scale() + SETTINGS.ZOOM_INCREMENT)
            # self.scene.item_group.setScale(group.scale() + SETTINGS.ZOOM_INCREMENT)
            self.scene.global_scale *= (1+SETTINGS.ZOOM_INCREMENT)
        else:
            self.point.setScale(self.point.scale() * (1-SETTINGS.ZOOM_INCREMENT))
            group.setScale(group.scale() - SETTINGS.ZOOM_INCREMENT)
            # self.scene.item_group.setScale(group.scale() - SETTINGS.ZOOM_INCREMENT)
            self.scene.global_scale *= (1-SETTINGS.ZOOM_INCREMENT)

        self.scene.destroyItemGroup(group)

        # print self.scene.global_scale

    def resizeEvent(self, event):
        self.setSceneRect(0, 0, self.width(), self.height())
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
