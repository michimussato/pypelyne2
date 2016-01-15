import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import src.modules.ui.graphicsview.graphicsview as graphicsview
import src.modules.ui.graphicsscene.graphicsscene as graphicsscene
import src.conf.settings.SETTINGS as SETTINGS


class GraphicsViewStage(graphicsview.GraphicsView):
    def __init__(self):
        super(GraphicsViewStage, self).__init__()
        self.scene = graphicsscene.GraphicsScene()
        self.setScene(self.scene)

        self.setMouseTracking(False)

        self.setDragMode(self.RubberBandDrag)

        self.point = QtGui.QGraphicsRectItem(-10, -10, 20, 20)
        self.scene.addItem(self.point)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.mouse_position_previous = QtCore.QPoint(0, 0)

    def mouseMoveEvent(self, event):
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

            # return

        self.mouse_position_previous = event_pos_scene

        return QtGui.QGraphicsView.mouseMoveEvent(self, event)

    # def mouseReleaseEvent(self, event):
    #     if self.dragMode() != self.RubberBandDrag:
    #         self.setDragMode(self.RubberBandDrag)

        # return QtGui.QGraphicsView.mousePressEvent(self, event)

    def wheelEvent(self, event):
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

        return QtGui.QGraphicsView.wheelEvent(self, event)

    def resizeEvent(self, event):
        self.setSceneRect(0, 0, self.width(), self.height())
        self.scene.base_rect.setRect(QtCore.QRectF(self.rect()))

        return QtGui.QGraphicsView.resizeEvent(self, event)
