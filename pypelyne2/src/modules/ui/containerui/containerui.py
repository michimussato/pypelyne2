import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import logging
import random
import pypelyne2.src.modules.ui.graphicsscene.graphicsscenenodes as graphicsscenenodes
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.parser.parse_containers as parse_containers
import pypelyne2.src.modules.ui.qgraphicsproxywidgetnowheel.qgraphicsproxywidgetnowheel as qgraphicsproxywidgetnowheel
import pypelyne2.src.modules.ui.navigator.navigator as navigator


class ContainerUI(QtGui.QGraphicsItem):
    def __init__(self, position=QtCore.QPoint(0, 0), container=None, scene_object=None):
        super(ContainerUI, self).__init__()

        reload(SETTINGS)

        self.scene_object = scene_object

        self.view_object = self.scene_object.view_object

        self.nodes_scene = graphicsscenenodes.GraphicsSceneNodes(view_object=self.view_object)

        self.navigator_nodes = navigator.Navigator(scene_object=self.nodes_scene,
                                                   view_object=self.scene_object.view_object)

        self.container = container or parse_containers.get_containers()[random.randint(0, len(parse_containers.get_containers())-1)]

        self.rect = QtCore.QRectF(0, 0, 100, 100)

        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)

        self.setAcceptHoverEvents(True)

        self.container_color_item = QtGui.QColor(0, 0, 0)

        self.setPos(position)

        self.hovered = False

        self.child_nodes = []
        self.output_list = []
        self.input_list = []

        self.connections = []

        self.widget = QtGui.QWidget()

        self.set_container_color()

        self.widget_proxy = qgraphicsproxywidgetnowheel.QGraphicsProxyWidgetNoWheel()

    def add_ui_elements(self):
        self.widget_proxy.setWidget(self.widget)
        self.widget_proxy.setParentItem(self)

    def paint(self, painter, option, widget):

        painter.setRenderHint(painter.Antialiasing)

        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(0)

        # hover_color = QtGui.QColor(255, 160, 0)
        #
        # if option.state & QtGui.QStyle.State_Selected:
        #     self.setZValue(1)
        #     pen.setWidth(3)
        #     pen.setColor(hover_color)
        #     self.gradient.setColorAt(0, self.task_color_item)
        #     self.gradient.setColorAt(1, self.task_color_item)
        #
        # elif option.state & QtGui.QStyle.State_MouseOver or self.hovered:
        #     pen.setWidth(2)
        #     self.setZValue(3)
        #
        #     pen.setColor(hover_color)
        #     self.gradient.setColorAt(0, self.task_color_item)
        #     self.gradient.setColorAt(1, self.task_color_item.darker(160))
        #
        # else:
        #     pen.setWidth(0)
        #     self.setZValue(0)
        #     self.gradient.setColorAt(0, self.task_color_item)
        #     self.gradient.setColorAt(1, self.task_color_item.darker(160))
        #
        # painter.setBrush(self.gradient)

        painter.setBrush(self.container_color_item)

        painter.setPen(pen)

        painter.drawRoundedRect(self.rect, SETTINGS.NODE_ROUNDNESS, SETTINGS.NODE_ROUNDNESS)

    def set_container_color(self):
        logging.info('ContainerUI.set_container_color() ({0})'.format(self))
        container_color = self.container.color
        self.container_color_item.setNamedColor(container_color)

    def boundingRect(self):
        return self.rect

    def hoverEnterEvent(self, event):
        logging.info('hoverEnterEvent on ContainerUI ({0})'.format(self))
        self.hovered = True

        return QtGui.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        logging.info('hoverLeaveEvent on ContainerUI ({0})'.format(self))
        self.hovered = False

        return QtGui.QGraphicsItem.hoverLeaveEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        logging.info('mouseDoubleClickEvent on ContainerUI ({0})'.format(self))

        self.scene_object.view_object.setScene(self.nodes_scene)

        self.nodes_scene.output_area.adjust_container()

        return QtGui.QGraphicsItem.mouseDoubleClickEvent(self, event)
