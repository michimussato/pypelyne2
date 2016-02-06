import uuid
import logging
import random
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import cPickle
import pypelyne2.src.modules.ui.compositeicon.compositeicon as compositeicon
import pypelyne2.src.modules.ui.porthover.porthover as porthover
import pypelyne2.src.parser.parse_outputs as parse_outputs
import pypelyne2.src.modules.ui.qgraphicsproxywidgetnowheel.qgraphicsproxywidgetnowheel as qgraphicsproxywidgetnowheel
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


# http://trevorius.com/scrapbook/python/pyqt-multiple-inheritance/
class Port(QtGui.QGraphicsItem):

    def __init__(self, node_object=None, output_object=None, port_id=None):
        super(Port, self).__init__()

        self.parent_node = node_object

        self.uuid = port_id or str(uuid.uuid4())

        self.setAcceptsHoverEvents(True)

        self.color_item = QtGui.QColor(255, 0, 0)

        self.output_object = output_object or parse_outputs.get_outputs()[random.randint(0, len(parse_outputs.get_outputs())-1)]

        self.pixmap = compositeicon.CompositeIconOutput(self.output_object).output_icon

        self.hovered = False

        self.moved = {'x': 0.0, 'y': 0.0}

        self.rect = QtCore.QRectF(-SETTINGS.OUTPUT_RADIUS/2,
                                  -SETTINGS.OUTPUT_RADIUS/2,
                                  SETTINGS.OUTPUT_RADIUS,
                                  SETTINGS.OUTPUT_RADIUS)

        self.widget_title = porthover.OutputHover(self.output_object)
        self.widget_title_proxy = qgraphicsproxywidgetnowheel.QGraphicsProxyWidgetNoWheel()
        self.add_ui_elements()
        self.set_label()
        self.set_color()

    # def set_opacity(self, opacity=1.0):
    #     self.setOpacity(opacity)
    #     for upstream_connection in self.upstream_connections:
    #         upstream_connection.setOpacity(opacity)

    def add_ui_elements(self):

        self.widget_title_proxy.setWidget(self.widget_title)
        self.widget_title_proxy.setParentItem(self)

        self.widget_title_proxy.setMaximumHeight(0.0)
        self.widget_title_proxy.setMaximumWidth(0.0)

    def set_color(self):
        self.color_item.setNamedColor(self.output_object.color)

    def boundingRect(self):
        return self.rect

    def set_label(self, name=None):

        self.widget_title.label_lock_icon.setPixmap(self.pixmap)

        self.widget_title.setVisible(SETTINGS.DISPLAY_OUTPUT_NAME)
        self.widget_title.label_title.setText(name or self.uuid)
        self.widget_title.label_title_edit.setText(name or self.uuid)
        self.widget_title.label_output.setText(self.output_object.abbreviation)

        # self.set_label_pos()

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(1)

        painter.setPen(pen)

        if self.hovered:
            painter.setBrush(QtGui.QBrush(self.color_item.lighter(SETTINGS.LIGHTER_AMOUNT)))
        else:
            painter.setBrush(QtGui.QBrush(self.color_item))

        painter.drawEllipse(self.rect)


class Output(Port):

    def __init__(self, node_object=None, output_object=None, port_id=None):
        super(Output, self).__init__(node_object, output_object, port_id)

        self.node_object = node_object

        self.downstream_ports = []

        self.downstream_connections = []

        self.drag_cursor = QtGui.QCursor(QtCore.Qt.OpenHandCursor)

        self.widget_title.label_title_edit.returnPressed.connect(self.update_title)

    def update_title(self, init=False):
        title = self.widget_title.label_title
        title_edit = self.widget_title.label_title_edit

        title_edit.setReadOnly(True)

        if init:
            new_title = self.uuid
        else:
            new_title = title_edit.text()

        title.setText(new_title)
        title_edit.setText(new_title)
        title_edit.setVisible(False)
        title.setVisible(True)
        self.widget_title_proxy.resize(0, 0)
        self.widget_title_proxy.adjustSize()

        self.set_label_pos()

    def set_label_pos(self):
        self.widget_title_proxy.setPos(-self.widget_title_proxy.rect().width()-SETTINGS.OUTPUT_RADIUS/2-SETTINGS.OUTPUT_SPACING,
                                       -self.widget_title_proxy.rect().height()/2)

    def hoverEnterEvent(self, event):
        logging.info('hoverEnterEvent on Output ({0})'.format(self))

        self.hovered = True
        for downstream_port in self.downstream_ports:
            downstream_port.hovered = True

        for downstream_connection in self.downstream_connections:
            downstream_connection.hovered = True

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

        self.widget_title_proxy.setMaximumHeight(16777215.0)
        self.widget_title_proxy.setMaximumWidth(16777215.0)

        self.widget_title.setVisible(True)

        self.set_label_pos()

        return QtGui.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        logging.info('hoverLeaveEvent on Output ({0})'.format(self))

        self.hovered = False
        for downstream_port in self.downstream_ports:
            downstream_port.hovered = False

        for downstream_connection in self.downstream_connections:
            downstream_connection.hovered = False

        self.widget_title_proxy.setMaximumHeight(0.0)
        self.widget_title_proxy.setMaximumWidth(0.0)

        QtGui.QApplication.restoreOverrideCursor()

        self.widget_title.setVisible(SETTINGS.DISPLAY_OUTPUT_NAME)

        return QtGui.QGraphicsItem.hoverLeaveEvent(self, event)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on Output ({0})'.format(self))

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.RightButton:

            pos = event.pos()

            self.moveBy(pos.x(), pos.y())

            opacity = max(0, 1-(max(abs(self.moved['x']),
                                    abs(self.moved['y']))/SETTINGS.REMOVE_PORT_DISTANCE))

            self.set_opacity(opacity=opacity)

            self.moved['x'] += pos.x()
            self.moved['y'] += pos.y()

        elif event.buttons() == QtCore.Qt.LeftButton:

            logging.info('mouseMoveEvent on Output {0}'.format(self))
            # http://stackoverflow.com/questions/14395799/pyqt4-drag-and-drop
            mime_data = QtCore.QMimeData()
            mime_data.setObjectName('nodeoutput/draggable-output')

            objects_dict = dict()

            objects_dict['output_object'] = self.output_object
            objects_dict['output_graphicsitem_uuid'] = self.uuid

            pickled_output_object = cPickle.dumps(objects_dict.copy())
            mime_data.setData('nodeoutput/draggable-output', pickled_output_object)

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

    def remove_output(self):
        scene = self.scene()

        temp_list_copy = list(self.downstream_ports)

        for downstream_port in temp_list_copy:
            downstream_port.remove_input()

        self.parent_node.outputs.remove(self)

        del temp_list_copy

        self.parent_node.resize()

        scene.removeItem(self)

    def mouseReleaseEvent(self, event):

        if self.moved['x'] > SETTINGS.REMOVE_PORT_DISTANCE \
                or self.moved['x'] < -SETTINGS.REMOVE_PORT_DISTANCE \
                or self.moved['y'] > SETTINGS.REMOVE_PORT_DISTANCE \
                or self.moved['y'] < -SETTINGS.REMOVE_PORT_DISTANCE:
            # scene = self.scene()
            #
            # temp_list_copy = list(self.downstream_ports)
            #
            # for downstream_port in temp_list_copy:
            #     downstream_port.remove_input()
            #
            # self.parent_node.outputs.remove(self)
            #
            # del temp_list_copy
            #
            # self.parent_node.resize()
            #
            # scene.removeItem(self)

            self.remove_output()

        else:
            self.moveBy(-self.moved['x'], -self.moved['y'])

        self.moved = {'x': 0.0, 'y': 0.0}
        self.set_opacity()

    def set_opacity(self, opacity=1.0):
        self.setOpacity(opacity)
        for downstream_port in self.downstream_ports:
            downstream_port.set_opacity(opacity)


class Input(Port):
    # TODO: fix inheritance structure
    def __init__(self, node_object=None, output_object=None, port_id=None, start_item=None):
        super(Input, self).__init__(node_object, output_object, port_id)

        self.parent_node = node_object

        self.upstream_port = start_item

        # there can only be one, but maybe we can inherit...
        self.upstream_connections = []

        self.widget_title = porthover.InputHover(self.output_object)
        self.add_ui_elements()

        self.set_label(name=self.upstream_port.widget_title.label_title.text())

    def set_label_pos(self):
        self.widget_title_proxy.setPos(SETTINGS.OUTPUT_RADIUS/2+SETTINGS.OUTPUT_SPACING,
                                       -self.widget_title_proxy.rect().height()/2)

    @property
    def output_label(self):
        upstream_node_name = self.upstream_port.node_object.widget_title.label_title.text()
        upstream_output_name = self.upstream_port.widget_title.label_title.text()
        return '{0}.{1}'.format(upstream_node_name, upstream_output_name)

    def hoverEnterEvent(self, event):
        logging.info('hoverEnterEvent on Input ({0})'.format(self))

        self.hovered = True
        self.upstream_port.hovered = True
        for upstream_connection in self.upstream_connections:
            upstream_connection.hovered = True

        self.widget_title.label_title.setText(self.output_label)

        self.widget_title_proxy.setMaximumHeight(16777215.0)
        self.widget_title_proxy.setMaximumWidth(16777215.0)

        self.widget_title.setVisible(True)
        
        self.widget_title_proxy.adjustSize()

        self.set_label_pos()

        return QtGui.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        logging.info('hoverLeaveEvent on Input ({0})'.format(self))

        self.hovered = False
        self.upstream_port.hovered = False
        for upstream_connection in self.upstream_connections:
            upstream_connection.hovered = False

        self.widget_title_proxy.setMaximumHeight(0.0)
        self.widget_title_proxy.setMaximumWidth(0.0)

        self.widget_title.setVisible(SETTINGS.DISPLAY_OUTPUT_NAME)

        return QtGui.QGraphicsItem.hoverLeaveEvent(self, event)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on Input ({0})'.format(self))

    def mouseMoveEvent(self, event):
        logging.info('mouseMoveEvent on Input {0}'.format(self))

    def mouseMoveEvent(self, event):

        if event.buttons() == QtCore.Qt.RightButton:

            pos = event.pos()

            self.moveBy(pos.x(), pos.y())

            opacity = max(0, 1-(max(abs(self.moved['x']),
                                    abs(self.moved['y']))/SETTINGS.REMOVE_PORT_DISTANCE))

            self.set_opacity(opacity=opacity)

            self.moved['x'] += pos.x()
            self.moved['y'] += pos.y()

        elif event.buttons() == QtCore.Qt.LeftButton:

            logging.info('mouseMoveEvent on Output {0}'.format(self))
            # http://stackoverflow.com/questions/14395799/pyqt4-drag-and-drop
            mime_data = QtCore.QMimeData()
            mime_data.setObjectName('nodeoutput/draggable-output')

            objects_dict = dict()

            objects_dict['output_object'] = self.output_object
            objects_dict['output_graphicsitem_uuid'] = self.uuid

            pickled_output_object = cPickle.dumps(objects_dict.copy())
            mime_data.setData('nodeoutput/draggable-output', pickled_output_object)

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

            # QtGui.QApplication.restoreOverrideCursor()

        else:

            return QtGui.QGraphicsItem.mouseMoveEvent(self, event)

    def remove_input(self):
        # removes this input
        # removes the connection
        # removes this input from this node
        # removes the connection from this node

        scene = self.scene()

        for upstream_connection in self.upstream_connections:
            scene.removeItem(upstream_connection)
            self.upstream_port.hovered = False
            self.upstream_port.downstream_connections.remove(upstream_connection)
            self.parent_node.connections.remove(upstream_connection)
            scene.connection_items.remove(upstream_connection)
            scene.removeItem(upstream_connection)

        self.upstream_port.downstream_ports.remove(self)

        self.parent_node.inputs.remove(self)

        self.parent_node.resize()

        scene.removeItem(self)

    def mouseReleaseEvent(self, event):

        if self.moved['x'] > SETTINGS.REMOVE_PORT_DISTANCE \
                or self.moved['x'] < -SETTINGS.REMOVE_PORT_DISTANCE \
                or self.moved['y'] > SETTINGS.REMOVE_PORT_DISTANCE \
                or self.moved['y'] < -SETTINGS.REMOVE_PORT_DISTANCE:

            self.remove_input()

        else:
            self.moveBy(-self.moved['x'], -self.moved['y'])

        self.moved = {'x': 0.0, 'y': 0.0}
        self.set_opacity()

    def set_opacity(self, opacity=1.0):
        self.setOpacity(opacity)
        for upstream_connection in self.upstream_connections:
            upstream_connection.setOpacity(opacity)
