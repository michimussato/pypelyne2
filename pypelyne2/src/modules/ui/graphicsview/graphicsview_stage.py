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
        self.viewport().setCursor(self.cursor)

        self.setMouseTracking(False)

        self.setDragMode(self.RubberBandDrag)

        self.point = QtGui.QGraphicsRectItem(-10, -10, 20, 20)
        self.scene.addItem(self.point)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.mouse_position_previous = QtCore.QPoint(0, 0)

        self.screen_representation = None
        self.scene_representation = None

        self.navigator()

    def navigator(self):
        self.screen_representation = QtGui.QGraphicsRectItem(0,
                                                             0,
                                                             self.scene.itemsBoundingRect().width() * SETTINGS.NAVIGATOR_SCALE,
                                                             self.scene.itemsBoundingRect().height() * SETTINGS.NAVIGATOR_SCALE)

        self.scene.addItem(self.screen_representation)

        self.screen_representation.setZValue(1000.0)

        self.scene_representation = QtGui.QGraphicsRectItem(0,
                                                            0,
                                                            self.scene.itemsBoundingRect().width() * SETTINGS.NAVIGATOR_SCALE,
                                                            self.scene.itemsBoundingRect().height() * SETTINGS.NAVIGATOR_SCALE)

        self.scene.addItem(self.scene_representation)
        self.scene_representation.setZValue(1000.0)
        self.screen_representation.setParentItem(self.scene_representation)

        color_navigator_rect = QtGui.QColor(SETTINGS.NAVIGATOR_R*255,
                                            SETTINGS.NAVIGATOR_G*255,
                                            SETTINGS.NAVIGATOR_B*255,
                                            SETTINGS.NAVIGATOR_ALPHA*255)
        color_screen_rect = QtGui.QColor(255-SETTINGS.NAVIGATOR_R*255,
                                         255-SETTINGS.NAVIGATOR_G*255,
                                         255-SETTINGS.NAVIGATOR_B*255,
                                         SETTINGS.NAVIGATOR_ALPHA*255)
        brush_navigator_rect = QtGui.QBrush(color_screen_rect)
        brush_screen_rect = QtGui.QBrush(color_navigator_rect)
        self.screen_representation.setBrush(brush_navigator_rect)
        self.scene_representation.setBrush(brush_screen_rect)

    def adjust_navigator(self):

        # print self.mapToScene(self.navigator_rect.rect().right(), self.navigator_rect.rect().bottom())

        self.screen_representation.setRect(0,
                                           0,
                                           self.viewport().width() * SETTINGS.NAVIGATOR_SCALE,
                                           self.viewport().height() * SETTINGS.NAVIGATOR_SCALE)

        # magic function:
        relative_rect = self.mapFromScene(self.scene.itemsBoundingRect()).boundingRect()
        # print relative_rect.topLeft()
        # print relative_rect.bottomLeft()
        # print relative_rect.topRight()
        # print relative_rect.bottomRight()

        self.scene_representation.setRect(relative_rect.x() * SETTINGS.NAVIGATOR_SCALE,
                                          relative_rect.y() * SETTINGS.NAVIGATOR_SCALE,
                                          relative_rect.width() * SETTINGS.NAVIGATOR_SCALE,
                                          relative_rect.height() * SETTINGS.NAVIGATOR_SCALE)

        self.scene_representation.setPos(self.viewport().width() - self.scene_representation.rect().width() - self.scene_representation.rect().topLeft().x(),
                                         self.viewport().height() - self.scene_representation.rect().height() - self.scene_representation.rect().topLeft().y())

        if self.scene_representation.rect().width()-self.screen_representation.rect().width() > 1.0\
                or self.scene_representation.rect().height()-self.screen_representation.rect().height() > 1.0:
            self.scene_representation.setVisible(True)
        else:
            self.scene_representation.setVisible(False)

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
                self.setDragMode(self.NoDrag)
                group = self.scene.createItemGroup(self.scene.node_items)
                self.point.setPos(event_pos_scene)
                group.translate(-1*delta.x(), -1*delta.y())
                self.scene.destroyItemGroup(group)
                # self.setDragMode(self.RubberBandDrag)

            self.mouse_position_previous = event_pos_scene

            self.adjust_navigator()

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

            self.adjust_navigator()

            return QtGui.QGraphicsView.wheelEvent(self, event)

    def resizeEvent(self, event):
        self.setSceneRect(0, 0, self.width(), self.height())
        self.scene.base_rect.setRect(QtCore.QRectF(self.rect()))

        self.adjust_navigator()

        return QtGui.QGraphicsView.resizeEvent(self, event)
