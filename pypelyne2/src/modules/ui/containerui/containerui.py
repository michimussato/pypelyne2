import cPickle
import logging

import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import pypelyne2.src.core.entities.uuidobject as uuidobject
import pypelyne2.src.modules.containercore.containercore as containercore

import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.modules.ui.compositeicon.compositeicon as compositeicon
import pypelyne2.src.modules.ui.navigator.navigator as navigator
import pypelyne2.src.modules.ui.qgraphicsproxywidgetnowheel.qgraphicsproxywidgetnowheel as qgraphicsproxywidgetnowheel


# class ContainterUIWidgetTitle(nodeui.WidgetNode):
#
#     """Might be used to create a more advanced title to ContainerUI."""
#
#     def __init__(self, node_object=None):
#         super(ContainterUIWidgetTitle, self).__init__()
#
#         self.node = node_object
#
#         self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
#                                           'src',
#                                           'modules',
#                                           'ui',
#                                           'containerui',
#                                           'containerui_widget_title.ui'), self)
#
#         self.set_palette()
#
#         self.preview_icon = labelgif.LabelGif(self.node)
#
#         self.setup_title()
#
#     def setup_title(self):
#         self.ui.label_title.setToolTip('shift+left click to change name')
#         self.ui.label_title_edit.setToolTip('enter to submit')
#         self.ui.label_title_edit.setText(self.ui.label_title.text())
#
#         self.ui.label_title.setVisible(False)
#         self.ui.label_title_edit.setVisible(True)
#
#         self.ui.vlayout_preview.addWidget(self.preview_icon)
#
#     def mousePressEvent(self, event):
#         logging.info('mousePressEvent on OutputHover ({0})'.format(self))
#         keyboard_modifiers = QtGui.QApplication.keyboardModifiers()
#
#         if keyboard_modifiers == QtCore.Qt.ShiftModifier and event.button() == QtCore.Qt.LeftButton:
#             self.ui.label_title.setVisible(False)
#             self.ui.label_title_edit.setVisible(True)
#             self.ui.label_title_edit.setReadOnly(False)
#             self.ui.label_title_edit.setFocus()
#             self.ui.label_title_edit.selectAll()
#
#         return nodeui.WidgetNode.mouseMoveEvent(self, event)


class Input(uuidobject.UuidObject, QtGui.QGraphicsEllipseItem):

    """The output port of the ContainerUI."""

    def __init__(self, container=None):

        super(Input, self).__init__()

        self.container = container

        self.container_object = self.container.container

        # self.upstream_containers = []

        self.pixmap = compositeicon.CompositeIconOutput(self.container_object).output_icon

        self.setParentItem(self.container)

        self.inputs = []

        self.setAcceptHoverEvents(True)

        self.setStartAngle(90*16)
        self.setSpanAngle(180*16)

        self.setToolTip(self.object_id)

        self.setRect(-SETTINGS.CONTAINER_PORT_RADIUS/2,
                     -SETTINGS.CONTAINER_PORT_RADIUS/2,
                     SETTINGS.CONTAINER_PORT_RADIUS,
                     SETTINGS.CONTAINER_PORT_RADIUS)


class Output(uuidobject.UuidObject, QtGui.QGraphicsEllipseItem):

    """The output port of the ContainerUI."""

    def __init__(self, container=None):

        super(Output, self).__init__()

        self.container = container

        self.container_object = self.container.container

        self.pixmap = compositeicon.CompositeIconOutput(self.container_object).output_icon

        self.setParentItem(self.container)

        # self.outputs = []
        self.outputs = set()

        self.setAcceptHoverEvents(True)

        self.setStartAngle(-90*16)
        self.setSpanAngle(180*16)

        self.setToolTip(self.object_id)

        self.setRect(-SETTINGS.CONTAINER_PORT_RADIUS/2*SETTINGS.CONTAINER_OUTPUT_MULT,
                     -SETTINGS.CONTAINER_PORT_RADIUS/2*SETTINGS.CONTAINER_OUTPUT_MULT,
                     SETTINGS.CONTAINER_PORT_RADIUS*SETTINGS.CONTAINER_OUTPUT_MULT,
                     SETTINGS.CONTAINER_PORT_RADIUS*SETTINGS.CONTAINER_OUTPUT_MULT)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on ContainerOutput ({0})'.format(self))

    def mouseMoveEvent(self, event):
        # if event.buttons() == QtCore.Qt.RightButton:
        #
        #     pos = event.pos()
        #
        #     self.moveBy(pos.x(), pos.y())
        #
        #     opacity = max(0, 1-(max(abs(self.moved['x']),
        #                             abs(self.moved['y']))/SETTINGS.REMOVE_PORT_DISTANCE))
        #
        #     self.set_opacity(opacity=opacity)
        #
        #     self.moved['x'] += pos.x()
        #     self.moved['y'] += pos.y()

        if event.buttons() == QtCore.Qt.LeftButton:

            logging.info('mouseMoveEvent on ContainerOutput {0}'.format(self))
            # http://stackoverflow.com/questions/14395799/pyqt4-drag-and-drop
            mime_data = QtCore.QMimeData()
            mime_data.setObjectName('containeroutput/draggable-output')

            objects_dict = dict()

            objects_dict[u'output_graphicsitem_uuid'] = self.object_id
            # objects_dict[u'node'] = self

            pickled_container_object = cPickle.dumps(objects_dict.copy())
            mime_data.setData('containeroutput/draggable-output', pickled_container_object)

            icon = QtGui.QLabel()

            icon.setPixmap(self.pixmap)

            drag = QtGui.QDrag(icon)
            drag.setMimeData(mime_data)
            drag.setPixmap(self.pixmap)

            if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
                pass
            #     print 'moved'
            # else:
            #     print 'copied'

        else:
            return QtGui.QGraphicsItem.mouseMoveEvent(self, event)

    def dropEvent(self, event):
        logging.info('dropEvent on {0}'.format(self))


class ContainerUI(containercore.ContainerCore, QtGui.QGraphicsItem):

    """This is the actual asset container."""

    def __init__(self, puppeteer, container_object, main_scene, position=QtCore.QPoint(0, 0)):

        super(ContainerUI, self).__init__(puppeteer=puppeteer,
                                          container_object=container_object,
                                          main_scene=main_scene)

        reload(SETTINGS)

        self.navigator_nodes = navigator.Navigator(scene_object=self.container_scene,
                                                   view_object=self.main_scene.view_object)

        self.rect = QtCore.QRectF()

        # self.upstream_containers = []

        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)

        self.setAcceptHoverEvents(True)

        self.container_color_item = QtGui.QColor(0, 0, 0)

        self.setPos(position)

        self.hovered = False

        self.widget = QtGui.QWidget()
        self.widget_proxy = qgraphicsproxywidgetnowheel.QGraphicsProxyWidgetNoWheel()

        self.set_container_color()

        self.text_label = QtGui.QGraphicsTextItem()
        self.text_label.setParentItem(self)

        self.text_connected_containers = QtGui.QGraphicsTextItem()
        self.text_connected_containers.setParentItem(self)

        self.text_inputs = QtGui.QGraphicsTextItem()
        self.text_inputs.setParentItem(self)

        self.text_outputs = QtGui.QGraphicsTextItem()
        self.text_outputs.setParentItem(self)

        self.input_port = Input(container=self)
        # self.inputs = []
        # self.input_port.setParentItem(self)
        # self.input_port.setToolTip()
        self.output_port = Output(container=self)
        self.outputs.append(self.output_port)
        # self.output_port.setParentItem(self)
        # self.rect_port = QtCore.QRectF()

        # self.setup_ports()

        self.update_label()

    # def setup_ports(self):
    #
    #     """Adds the input and output area of the ContainerUI."""
    #
    #     self.rect_port.setRect(-SETTINGS.CONTAINER_OUTPUT_RADIUS/2,
    #                            -SETTINGS.CONTAINER_OUTPUT_RADIUS/2,
    #                            SETTINGS.CONTAINER_OUTPUT_RADIUS,
    #                            SETTINGS.CONTAINER_OUTPUT_RADIUS)
    #
    #     self.input_port.setRect(self.rect_port)
    #     # self.input_port.setStartAngle(90*16)
    #     # self.input_port.setSpanAngle(180*16)
    #
    #     self.output_port.setRect(self.rect_port)
    #     # self.output_port.setStartAngle(-90*16)
    #     # self.output_port.setSpanAngle(180*16)

    def remove_container_output_channel(self, portwidget):

        self.container_output_channels.remove(portwidget)
        self.update_label()

    def connect_internal(self, output_object, node):

        """Connect output with a node"""

        pass

    def connect(self, destination_container):

        """Connect self to downstream ContainerUI"""

        pass

    # def create_node(self, plugin):
    #
    #     """Create a new node inside self (NodeUI)"""
    #
    #     pass

    def add_node(self, node):

        """Add an existing node to self (NodeUI)"""

        pass

    # def update_inputs_source_area(self):
    #
    #     self.container_scene.output_area.inputs
    #
    #     for upstream_container in self.upstream_containers:
    #         # print upstream_container.output_port
    #         # for output in upstream_container.output_port.outputs:
    #         #     print dir(output)
    #         # print upstream_container.container_scene.output_area.inputs
    #         for input_item in upstream_container.container_scene.output_area.inputs:
    #
    #             print dir(input_item)
    #
    #             self.puppeteer.create_asset_input(container=self,
    #                                               start_port_id=input_item.object_id)
    #
    #             # self.container_scene.input_area.add_output(input_item.output_object, input_item.object_id)
    #
    #             # add_output
    #
    #         # print upstream_container.output_port.outputs
    #
    #     # print self.inputs
    #
    #     # print 'herereere'
    #     # for upstream_container in self.upstream_containers:
    #     #     print upstream_container
    #     #     print upstream_container.output_port.outputs
    #
    #     # print 'herereere', self.input_port.inputs
    #     # for input in self.outputs:


    def update_label(self):

        # print 'container inputs  =', self.input_port.inputs
        # print 'container outputs =', self.output_port.outputs

        """updates the labels of the ContainerUI (name, inputs, outputs)"""

        if bool(self.output_port.outputs):
            self.output_port.setBrush(self.container_color_item.lighter(SETTINGS.LIGHTER_AMOUNT))
            self.output_port.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        else:
            self.output_port.setBrush(self.container_color_item.darker(SETTINGS.DARKER_AMOUNT))
            self.output_port.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

        if bool(self.input_port.inputs):
            self.input_port.setBrush(self.container_color_item.lighter(SETTINGS.LIGHTER_AMOUNT))
        else:
            self.input_port.setBrush(self.container_color_item.darker(SETTINGS.DARKER_AMOUNT))

        self.text_label.setPlainText('{0} (name: {1})'.format(self.container.type, self.name_string))
        self.text_connected_containers.setPlainText('upstream containers: {0}'.format(len(self.upstream_containers)))

        length = 0

        for upstream_container in self.upstream_containers:

            length += len(upstream_container.output_port.outputs)

            # for output in upstream_container.output_port.outputs:
            #     le

        self.text_inputs.setPlainText('inputs: {0}'.format(length))
        self.text_outputs.setPlainText('outputs: {0}'.format(len(self.output_port.outputs)))
        self.text_connected_containers.setY(self.text_label.boundingRect().height())
        self.text_inputs.setY(self.text_label.boundingRect().height() + self.text_connected_containers.boundingRect().height())
        self.text_outputs.setY(self.text_label.boundingRect().height() + self.text_connected_containers.boundingRect().height() + self.text_inputs.boundingRect().height())
        # self.text_inputs.setY(self.text_label.boundingRect().height())
        # for container_output_channel in self.container_output_channels:
        #     position = QtCore.QPointF(self.boundingRect().width(),
        #                               (self.container_output_channels.index(container_output_channel)*(SETTINGS.OUTPUT_RADIUS+SETTINGS.OUTPUT_SPACING)))
        #
        #     container_output_channel.setPos(position)

        self.resize()

    def resize(self):

        self.rect.setRect(0, 0, self.text_label.boundingRect().width(), self.childrenBoundingRect().height())

        self.input_port.setPos(0, self.boundingRect().height()/2)
        self.output_port.setPos(self.boundingRect().width(), self.boundingRect().height()/2)

        self.drop_area.setRect(self.boundingRect())

        # print self.drop_area.rect()

    # def boundingRect(self):
    #     return self.rect

    def add_ui_elements(self):

        """Adds the title widget. Not currently in use."""

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

        # self.resize()

    def set_container_color(self):

        """Set the container color based on container_object.color"""

        logging.info('ContainerUI.set_container_color() ({0})'.format(self))
        container_color = self.container.color
        self.container_color_item.setNamedColor(container_color)

    def boundingRect(self):

        """Needed to be reimplemented"""

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

        self.main_scene.view_object.setScene(self.container_scene)

        self.container_scene.output_area.resize()
        self.container_scene.input_area.adjust_container()
        self.container_scene.label_area.adjust_container()

        return QtGui.QGraphicsItem.mouseDoubleClickEvent(self, event)

    def keyPressEvent(self, event):
        logging.info('container.keyPressEvent() ({0})'.format(self))
        if event.key() == QtCore.Qt.Key_Backspace:
            self.puppeteer.delete_container(container=self)
