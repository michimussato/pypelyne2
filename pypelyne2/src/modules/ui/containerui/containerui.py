import os
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import PyQt4.uic as uic
import logging
import random
import pypelyne2.src.modules.ui.graphicsscene.graphicsscenenodes as graphicsscenenodes
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.parser.parse_containers as parse_containers
import pypelyne2.src.modules.ui.qgraphicsproxywidgetnowheel.qgraphicsproxywidgetnowheel as qgraphicsproxywidgetnowheel
import pypelyne2.src.modules.ui.navigator.navigator as navigator
import pypelyne2.src.modules.containercore.containercore as containercore
import pypelyne2.src.modules.ui.nodeui.nodeui as nodeui
import pypelyne2.src.modules.ui.labelgif.labelgif as labelgif


class ContainterUIWidgetTitle(nodeui.WidgetNode):
    def __init__(self, node_object=None):
        super(ContainterUIWidgetTitle, self).__init__()

        self.node = node_object

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'containerui',
                                          'containerui_widget_title.ui'), self)

        self.set_palette()

        self.preview_icon = labelgif.LabelGif(self.node)

        self.setup_title()

    def setup_title(self):
        self.ui.label_title.setToolTip('shift+left click to change name')
        self.ui.label_title_edit.setToolTip('enter to submit')
        self.ui.label_title_edit.setText(self.ui.label_title.text())

        self.ui.label_title.setVisible(False)
        self.ui.label_title_edit.setVisible(True)

        self.ui.vlayout_preview.addWidget(self.preview_icon)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on OutputHover ({0})'.format(self))
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()

        if keyboard_modifiers == QtCore.Qt.ShiftModifier and event.button() == QtCore.Qt.LeftButton:
            self.ui.label_title.setVisible(False)
            self.ui.label_title_edit.setVisible(True)
            self.ui.label_title_edit.setReadOnly(False)
            self.ui.label_title_edit.setFocus()
            self.ui.label_title_edit.selectAll()

        return nodeui.WidgetNode.mouseMoveEvent(self, event)


class ContainerUI(containercore.ContainerCore, QtGui.QGraphicsItem):
    def __init__(self, position=QtCore.QPoint(0, 0), container=None, scene_object=None):
        super(ContainerUI, self).__init__()

        reload(SETTINGS)
        
        # this is the main scene of the mainwindow. maybe rename
        self.scene_object = scene_object

        self.view_object = self.scene_object.view_object

        self.nodes_scene = graphicsscenenodes.GraphicsSceneNodes(view_object=self.view_object, container_object=self)

        self.navigator_nodes = navigator.Navigator(scene_object=self.nodes_scene,
                                                   view_object=self.scene_object.view_object)

        self.container = container or parse_containers.get_containers()[random.randint(0, len(parse_containers.get_containers())-1)]

        self.rect = QtCore.QRectF()

        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)

        self.setAcceptHoverEvents(True)

        self.container_color_item = QtGui.QColor(0, 0, 0)

        self.setPos(position)

        self.hovered = False

        self.container_output_channels = []
        self.container_input_channels = []

        self.child_nodes = []
        self.output_list = []
        self.input_list = []

        self.connections = []

        self.widget = QtGui.QWidget()
        self.widget_proxy = qgraphicsproxywidgetnowheel.QGraphicsProxyWidgetNoWheel()

        self.set_container_color()

        self.text_label = QtGui.QGraphicsTextItem()
        self.text_label.setParentItem(self)

        self.text_inputs = QtGui.QGraphicsTextItem()
        self.text_inputs.setParentItem(self)

        self.text_outputs = QtGui.QGraphicsTextItem()
        self.text_outputs.setParentItem(self)

        self.input_port = QtGui.QGraphicsEllipseItem()
        self.input_port.setParentItem(self)
        self.output_port = QtGui.QGraphicsEllipseItem()
        self.output_port.setParentItem(self)
        self.rect_port = QtCore.QRectF()

        self.setup_ports()

        self.update_label()

    def setup_ports(self):

        self.rect_port.setRect(-SETTINGS.CONTAINER_OUTPUT_RADIUS/2,
                               -SETTINGS.CONTAINER_OUTPUT_RADIUS/2,
                               SETTINGS.CONTAINER_OUTPUT_RADIUS,
                               SETTINGS.CONTAINER_OUTPUT_RADIUS)

        self.input_port.setRect(self.rect_port)
        self.input_port.setStartAngle(90*16)
        self.input_port.setSpanAngle(180*16)

        self.output_port.setRect(self.rect_port)
        self.output_port.setStartAngle(-90*16)
        self.output_port.setSpanAngle(180*16)

    def remove_container_output_channel(self, portwidget):
        self.container_output_channels.remove(portwidget)
        self.update_label()

    def update_label(self):

        if bool(self.container_output_channels):
            self.output_port.setBrush(self.container_color_item.lighter(SETTINGS.LIGHTER_AMOUNT))
            self.output_port.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        else:
            self.output_port.setBrush(self.container_color_item.darker(SETTINGS.DARKER_AMOUNT))
            self.output_port.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

        if bool(self.container_input_channels):
            self.input_port.setBrush(self.container_color_item.lighter(SETTINGS.LIGHTER_AMOUNT))
        else:
            self.input_port.setBrush(self.container_color_item.darker(SETTINGS.DARKER_AMOUNT))

        self.text_label.setPlainText('{0} (name: {1})'.format(self.container.type, self.name_string))
        self.text_inputs.setPlainText('inputs: {0}'.format(len(self.container_input_channels)))
        self.text_outputs.setPlainText('outputs: {0}'.format(len(self.container_output_channels)))
        self.text_inputs.setY(self.text_label.boundingRect().height())
        self.text_outputs.setY(self.text_label.boundingRect().height() + self.text_inputs.boundingRect().height())
        # self.text_inputs.setY(self.text_label.boundingRect().height())
        # for container_output_channel in self.container_output_channels:
        #     position = QtCore.QPointF(self.boundingRect().width(),
        #                               (self.container_output_channels.index(container_output_channel)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING)))
        #
        #     container_output_channel.setPos(position)

        self.rect.setRect(0, 0, self.text_label.boundingRect().width(), self.childrenBoundingRect().height())

        self.input_port.setPos(0, self.boundingRect().height()/2)
        self.output_port.setPos(self.boundingRect().width(), self.boundingRect().height()/2)

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
        self.nodes_scene.input_area.adjust_container()
        self.nodes_scene.label_area.adjust_container()

        return QtGui.QGraphicsItem.mouseDoubleClickEvent(self, event)
