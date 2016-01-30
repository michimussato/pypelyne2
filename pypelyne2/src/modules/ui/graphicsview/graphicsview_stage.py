import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.modules.ui.graphicsview.graphicsview as graphicsview
import pypelyne2.src.modules.ui.graphicsscene.graphicsscene as graphicsscene
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class GraphicsViewStage(graphicsview.GraphicsView):
    def __init__(self):
        super(GraphicsViewStage, self).__init__()
        self.scene = graphicsscene.GraphicsScene(self)
        self.setScene(self.scene)

        self.cursor = QtGui.QCursor(QtCore.Qt.CrossCursor)
        # QtGui.QApplication.setCur(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.viewport().setCursor(self.cursor)

        self.setMouseTracking(False)

        self.setDragMode(self.RubberBandDrag)

        self.point = QtGui.QGraphicsRectItem(-10, -10, 20, 20)
        self.scene.addItem(self.point)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.mouse_position_previous = QtCore.QPoint(0, 0)

        self.navigator_rect = None
        self.screen_rect = None

        self.navigator()

    def navigator(self):
        self.navigator_rect = QtGui.QGraphicsRectItem(0,
                                                      0,
                                                      self.scene.itemsBoundingRect().width()*SETTINGS.NAVIGATOR_SCALE,
                                                      self.scene.itemsBoundingRect().height()*SETTINGS.NAVIGATOR_SCALE)

        self.scene.addItem(self.navigator_rect)
        self.navigator_rect.setZValue(1000.0)

        self.screen_rect = QtGui.QGraphicsRectItem(0,
                                                   0,
                                                   self.scene.itemsBoundingRect().width()*SETTINGS.NAVIGATOR_SCALE,
                                                   self.scene.itemsBoundingRect().height()*SETTINGS.NAVIGATOR_SCALE)

        self.scene.addItem(self.screen_rect)
        self.screen_rect.setZValue(1000.0)
        self.navigator_rect.setParentItem(self.screen_rect)

    def adjust_navigator(self):

        self.navigator_rect.setRect(0,
                                    0,
                                    self.viewport().width()*SETTINGS.NAVIGATOR_SCALE,
                                    self.viewport().height()*SETTINGS.NAVIGATOR_SCALE)

        relative_rect = self.mapFromScene(self.scene.itemsBoundingRect()).boundingRect()
        # print relative_rect.topLeft()
        # print relative_rect.bottomLeft()
        # print relative_rect.topRight()
        # print relative_rect.bottomRight()

        self.screen_rect.setRect(relative_rect.x()*SETTINGS.NAVIGATOR_SCALE,
                                 relative_rect.y()*SETTINGS.NAVIGATOR_SCALE,
                                 relative_rect.width()*SETTINGS.NAVIGATOR_SCALE,
                                 relative_rect.height()*SETTINGS.NAVIGATOR_SCALE)

        self.screen_rect.setPos(self.viewport().width()-self.screen_rect.rect().width()-self.screen_rect.rect().topLeft().x(),
                                self.viewport().height()-self.screen_rect.rect().height()-self.screen_rect.rect().topLeft().y())

    def mouseMoveEvent(self, event):
        if self.hasFocus():
            self.setDragMode(self.RubberBandDrag)
            event_pos_scene = event.pos()
            previous_pos = self.mouse_position_previous
            delta = previous_pos - event_pos_scene

            mouse_modifiers = QtGui.QApplication.mouseButtons()
            keyboard_modifiers = QtGui.QApplication.keyboardModifiers()

            if mouse_modifiers == QtCore.Qt.MidButton \
                    or keyboard_modifiers == QtCore.Qt.ControlModifier and mouse_modifiers == QtCore.Qt.LeftButton:
                # QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
                self.setDragMode(self.NoDrag)
                group = self.scene.createItemGroup(self.scene.node_items)
                self.point.setPos(event_pos_scene)
                group.translate(-1*delta.x(), -1*delta.y())
                self.scene.destroyItemGroup(group)
                # self.setDragMode(self.RubberBandDrag)

                # return

            self.mouse_position_previous = event_pos_scene

            self.adjust_navigator()

            # QtGui.QApplication.restoreOverrideCursor()

            return QtGui.QGraphicsView.mouseMoveEvent(self, event)

    # def mousePressEvent(self, event):
    #     mouse_modifiers = QtGui.QApplication.mouseButtons()
    #     keyboard_modifiers = QtGui.QApplication.keyboardModifiers()
    #
    #     if mouse_modifiers == QtCore.Qt.MidButton \
    #             or keyboard_modifiers == QtCore.Qt.ControlModifier and mouse_modifiers == QtCore.Qt.LeftButton:
    #         QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
    #
    #     return QtGui.QGraphicsView.mousePressEvent(self, event)
    #
    # def mouseReleaseEvent(self, event):
    #     QtGui.QApplication.restoreOverrideCursor()
    # #     if self.dragMode() != self.RubberBandDrag:
    # #         self.setDragMode(self.RubberBandDrag)
    #
    #     return QtGui.QGraphicsView.mousePressEvent(self, event)

    def wheelEvent(self, event):
        if self.hasFocus():
            # QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

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

            # QtGui.QApplication.restoreOverrideCursor()

            self.adjust_navigator()

            return QtGui.QGraphicsView.wheelEvent(self, event)

    def resizeEvent(self, event):
        self.setSceneRect(0, 0, self.width(), self.height())
        self.scene.base_rect.setRect(QtCore.QRectF(self.rect()))

        self.adjust_navigator()

        return QtGui.QGraphicsView.resizeEvent(self, event)
