import os
import uuid
import logging
import random
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import PyQt4.uic as uic
import cPickle
import pypelyne2.src.modules.ui.compositeicon.compositeicon as compositeicon
import pypelyne2.src.parser.parse_outputs as parse_outputs
import pypelyne2.src.modules.ui.qgraphicsproxywidgetnowheel.qgraphicsproxywidgetnowheel as qgraphicsproxywidgetnowheel
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


# http://trevorius.com/scrapbook/python/pyqt-multiple-inheritance/
from pypelyne2.src.modules.ui import pixmapdraggable


class QWidgetOutput(QtGui.QWidget):
    def __init__(self, output_object=None):
        super(QWidgetOutput, self).__init__()

        self.output = output_object

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'output',
                                          'output_widget.ui'), self)

        self.palette = QtGui.QPalette()

    def set_palette(self):
        self.palette.setColor(QtGui.QWidget().backgroundRole(), QtGui.QColor(50, 50, 50, 0))
        if SETTINGS.TRANSPARENT_OUTPUT_LABEL:
            self.ui.setPalette(self.palette)

    def wheelEvent(self, event):
        logging.info('wheelEvent on QWidgetOutput ({0})'.format(self))
        event.ignore()


class QWidgetTitle(QWidgetOutput):
    def __init__(self, output_object=None):
        super(QWidgetTitle, self).__init__()

        self.output = output_object

        self.setup_title()

        # self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
        #                                   'src',
        #                                   'modules',
        #                                   'ui',
        #                                   'output',
        #                                   'output_widget.ui'), self)

    def setup_title(self):
        self.ui.label_title.setToolTip('shift+left click to change name')
        self.ui.label_title_edit.setToolTip('enter to submit')
        self.ui.label_title_edit.setText(self.ui.label_title.text())

        self.ui.label_title_edit.setVisible(False)
        self.ui.label_title.setVisible(True)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on QWidgetTitle ({0})'.format(self))
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()

        if keyboard_modifiers == QtCore.Qt.ShiftModifier and event.button() == QtCore.Qt.LeftButton:
            self.ui.label_title.setVisible(False)
            self.ui.label_title_edit.setVisible(True)
            self.ui.label_title_edit.setReadOnly(False)
            self.ui.label_title_edit.setFocus()
            self.ui.label_title_edit.selectAll()
            return

        return QWidgetTitle.mouseMoveEvent(self, event)


class QWidgetInput(QWidgetTitle):
    def __init__(self, output_object=None):
        super(QWidgetTitle, self).__init__()

        self.output = output_object

        self.set_palette()

        self.setup_title()

    def setup_title(self):
        self.ui.label_title.setToolTip('change name at output port')
        # self.ui.label_title_edit.setToolTip('enter to submit')
        self.ui.label_title_edit.setText(self.ui.label_title.text())

        self.ui.label_title_edit.setVisible(False)
        self.ui.label_title.setVisible(True)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on QWidgetTitle ({0})'.format(self))
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()

        if keyboard_modifiers == QtCore.Qt.ShiftModifier and event.button() == QtCore.Qt.LeftButton:
            return
        #     self.ui.label_title.setVisible(False)
        #     self.ui.label_title_edit.setVisible(True)
        #     self.ui.label_title_edit.setReadOnly(False)
        #     self.ui.label_title_edit.setFocus()
        #     self.ui.label_title_edit.selectAll()

        return QWidgetTitle.mouseMoveEvent(self, event)


class Port(QtGui.QGraphicsObject):

    def __init__(self, node_object=None, output_object=None, port_id=None):
        super(Port, self).__init__()

        self.node_object = node_object

        self.uuid = port_id or str(uuid.uuid4())

        self.setAcceptsHoverEvents(True)

        self.color_item = QtGui.QColor(255, 0, 0)

        self.output_object = output_object or parse_outputs.get_outputs()[random.randint(0, len(parse_outputs.get_outputs())-1)]

        self.pixmap = compositeicon.CompositeIconOutput(self.output_object).output_icon

        self.hovered = False

        self.rect = QtCore.QRectF(-SETTINGS.OUTPUT_RADIUS/2,
                                  -SETTINGS.OUTPUT_RADIUS/2,
                                  SETTINGS.OUTPUT_RADIUS,
                                  SETTINGS.OUTPUT_RADIUS)

        self.widget_title = QWidgetTitle(self.output_object)
        self.widget_title_proxy = qgraphicsproxywidgetnowheel.QGraphicsProxyWidgetNoWheel()
        self.add_ui_elements()
        self.set_label()
        self.set_color()

        self.set_label_pos()

    def add_ui_elements(self):

        self.widget_title_proxy.setWidget(self.widget_title)
        self.widget_title_proxy.setParentItem(self)

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

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(1)

        painter.setPen(pen)

        painter.setBrush(QtGui.QBrush(self.color_item))

        painter.drawEllipse(self.rect)


class Output(Port):

    def __init__(self, node_object=None, output_object=None, port_id=None):
        super(Output, self).__init__(node_object, output_object, port_id)

        self.node_object = node_object

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

    def set_label_pos(self):
        self.widget_title_proxy.setPos(-self.widget_title_proxy.rect().width()-SETTINGS.OUTPUT_RADIUS/2-SETTINGS.OUTPUT_SPACING,
                                       -self.widget_title_proxy.rect().height()/2)

    def hoverEnterEvent(self, event):
        logging.info('hoverEnterEvent on Output ({0})'.format(self))

        self.hovered = True

        self.set_label_pos()

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

        self.widget_title.setVisible(True)

        return QtGui.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        logging.info('hoverLeaveEvent on Output ({0})'.format(self))

        self.hovered = False

        self.widget_title_proxy.resize(0, 0)

        QtGui.QApplication.restoreOverrideCursor()

        self.widget_title.setVisible(SETTINGS.DISPLAY_OUTPUT_NAME)

        return QtGui.QGraphicsItem.hoverLeaveEvent(self, event)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on Output ({0})'.format(self))

    def mouseMoveEvent(self, event):
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

        return QtGui.QGraphicsItem.mouseMoveEvent(self, event)

    def dropEvent(self, event):
        logging.info('dropEvent on {0}'.format(self))


class Input(Port):
    # TODO: fix inheritance structure
    def __init__(self, node_object=None, output_object=None, port_id=None):
        super(Input, self).__init__(node_object, output_object, port_id)

        self.node_object = node_object

        self.widget_title = QWidgetInput(self.output_object)
        self.add_ui_elements()

        self.output_graphics_item = node_object.find_output_graphics_item(port_id)

        self.set_label(name=self.output_graphics_item.widget_title.label_title.text())

    def set_label_pos(self):
        self.widget_title_proxy.setPos(SETTINGS.OUTPUT_RADIUS/2+SETTINGS.OUTPUT_SPACING,
                                       -self.widget_title_proxy.rect().height()/2)

    @property
    def output_label(self):
        upstream_node_name = self.output_graphics_item.node_object.widget_title.label_title.text()
        upstream_output_name = self.output_graphics_item.widget_title.label_title.text()

        return '{0}.{1}'.format(upstream_node_name, upstream_output_name)

    def hoverEnterEvent(self, event):
        logging.info('hoverEnterEvent on Input ({0})'.format(self))

        self.hovered = True

        self.widget_title.label_title.setText(self.output_label)

        self.set_label_pos()

        self.widget_title.setVisible(True)

        return QtGui.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        logging.info('hoverLeaveEvent on Input ({0})'.format(self))

        self.hovered = False

        self.widget_title_proxy.resize(0, 0)

        self.widget_title.setVisible(SETTINGS.DISPLAY_OUTPUT_NAME)

        return QtGui.QGraphicsItem.hoverLeaveEvent(self, event)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on Input ({0})'.format(self))

    def mouseMoveEvent(self, event):
        logging.info('mouseMoveEvent on Input {0}'.format(self))
