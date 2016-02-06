import logging
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.modules.ui.graphicsview.graphicsview as graphicsview
import pypelyne2.src.modules.ui.graphicsscene.graphicsscene as graphicsscene
# import pypelyne2.src.modules.ui.container.container as container
import pypelyne2.src.modules.ui.navigator.navigator as navigator
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class GraphicsViewStage(graphicsview.GraphicsView):
    def __init__(self):
        super(GraphicsViewStage, self).__init__()
        self.scene_object = graphicsscene.GraphicsScene(self)
        self.setScene(self.scene_object)

        self.cursor = QtGui.QCursor(QtCore.Qt.CrossCursor)
        self.viewport().setCursor(self.cursor)

        self.setMouseTracking(False)

        self.setDragMode(self.RubberBandDrag)

        self.point = QtGui.QGraphicsRectItem(-10, -10, 20, 20)
        self.scene_object.addItem(self.point)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.mouse_position_previous = QtCore.QPoint(0, 0)

        self.screen_representation = None
        self.scene_representation = None

        self.navigator = navigator.Navigator(scene_object=self.scene_object,
                                             view_object=self)

        # self.container_inputs = container.Inputs(scene_object=self.scene_object,
        #                                          view_object=self)
        # self.container_outputs = container.Outputs(scene_object=self.scene_object,
        #                                            view_object=self)

    # def adjust_container(self):
    #     # self.container_inputs.adjust_container()
    #     # self.container_outputs.adjust_container()
    #     # pass

    def adjust_navigator(self):
        self.navigator.adjust_navigator()

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
                group = self.scene_object.createItemGroup(self.scene_object.node_items)
                self.point.setPos(event_pos_scene)
                group.translate(-1*delta.x(), -1*delta.y())

                self.scene_object.destroyItemGroup(group)

            self.mouse_position_previous = event_pos_scene

            if SETTINGS.ENABLE_NAVIGATOR:
                self.adjust_navigator()

            return QtGui.QGraphicsView.mouseMoveEvent(self, event)

    def wheelEvent(self, event):
        if self.hasFocus():
            group = self.scene_object.createItemGroup(self.scene_object.node_items)

            # absolute pos of mouse cursor in scene
            event_pos_scene = self.mapToScene(event.pos())

            self.point.setPos(event_pos_scene)

            group.setTransformOriginPoint(event_pos_scene)

            if event.delta() > 0:
                self.point.setScale(self.point.scale() * (1+SETTINGS.ZOOM_INCREMENT))
                group.setScale(group.scale() + SETTINGS.ZOOM_INCREMENT)
                self.scene_object.global_scale *= (1 + SETTINGS.ZOOM_INCREMENT)
            else:
                self.point.setScale(self.point.scale() * (1-SETTINGS.ZOOM_INCREMENT))
                group.setScale(group.scale() - SETTINGS.ZOOM_INCREMENT)
                self.scene_object.global_scale *= (1 - SETTINGS.ZOOM_INCREMENT)

            self.scene_object.destroyItemGroup(group)

            self.navigator.adjust_navigator()

            return QtGui.QGraphicsView.wheelEvent(self, event)

    def resizeEvent(self, event):
        logging.info('resizeEvent')
        self.setSceneRect(0, 0, self.width(), self.height())
        self.scene_object.base_rect.setRect(QtCore.QRectF(self.rect()))

        self.adjust_navigator()
        # self.adjust_container()

        return QtGui.QGraphicsView.resizeEvent(self, event)
