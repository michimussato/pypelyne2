import logging
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.modules.ui.graphicsview.graphicsview as graphicsview
import pypelyne2.src.modules.ui.graphicsscene.graphicsscenecontainer as graphicsscenecontainer
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class GraphicsViewStage(graphicsview.GraphicsView):
    def __init__(self):
        super(GraphicsViewStage, self).__init__()
        self.scene_object_containers = graphicsscenecontainer.GraphicsSceneContainer(self)

        self.set_container_scene()

        self.cursor = QtGui.QCursor(QtCore.Qt.CrossCursor)
        self.viewport().setCursor(self.cursor)

        self.setMouseTracking(False)

        self.setDragMode(self.RubberBandDrag)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.mouse_position_previous = QtCore.QPoint(0, 0)

        self.screen_representation = None
        self.scene_representation = None

    def adjust_container(self):
        scene = self.scene()

        if scene != self.scene_object_containers:
            scene.output_area.adjust_container()

    def set_container_scene(self):
        self.setScene(self.scene_object_containers)

    def adjust_navigator(self):
        scene = self.scene()

        scene.navigator.adjust_navigator()

    def mouseMoveEvent(self, event):
        logging.info('mouseMoveEvent on {0}'.format(self))

        scene = self.scene()

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
                group_nodes = scene.createItemGroup(scene.node_items)
                scene.point.setPos(event_pos_scene)
                group_nodes.translate(-1*delta.x(), -1*delta.y())

                scene.destroyItemGroup(group_nodes)

            self.mouse_position_previous = event_pos_scene

            if SETTINGS.ENABLE_NAVIGATOR:
                self.adjust_navigator()

            return QtGui.QGraphicsView.mouseMoveEvent(self, event)

    def wheelEvent(self, event):
        logging.info('wheelEvent on {0}'.format(self))

        scene = self.scene()

        if self.hasFocus():
            group_nodes = scene.createItemGroup(scene.node_items)

            event_pos_scene = self.mapToScene(event.pos())

            scene.point.setPos(event_pos_scene)

            group_nodes.setTransformOriginPoint(event_pos_scene)

            if event.delta() > 0:
                scene.point.setScale(scene.point.scale() * (1+SETTINGS.ZOOM_INCREMENT))
                group_nodes.setScale(group_nodes.scale() + SETTINGS.ZOOM_INCREMENT)
                self.scene().global_scale *= (1 + SETTINGS.ZOOM_INCREMENT)
            else:
                scene.point.setScale(scene.point.scale() * (1-SETTINGS.ZOOM_INCREMENT))
                group_nodes.setScale(group_nodes.scale() - SETTINGS.ZOOM_INCREMENT)
                self.scene().global_scale *= (1 - SETTINGS.ZOOM_INCREMENT)

            self.scene_object_containers.destroyItemGroup(group_nodes)

            scene.navigator.adjust_navigator()

            return QtGui.QGraphicsView.wheelEvent(self, event)

    def resizeEvent(self, event):
        logging.info('resizeEvent on {0}'.format(self))
        self.setSceneRect(0, 0, self.width(), self.height())
        self.scene().base_rect.setRect(QtCore.QRectF(self.rect()))

        self.adjust_navigator()
        self.adjust_container()

        return QtGui.QGraphicsView.resizeEvent(self, event)
