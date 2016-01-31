import os
import uuid
import logging
import random
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import PyQt4.uic as uic
import cPickle
import pypelyne2.src.modules.ui.compositeicon.compositeicon as compositeicon
import pypelyne2.src.modules.ui.pixmapdraggable.pixmapdraggable as pixmapdraggable
import pypelyne2.src.parser.parse_outputs as parse_outputs
import pypelyne2.src.modules.ui.qgraphicsproxywidgetnowheel.qgraphicsproxywidgetnowheel as qgraphicsproxywidgetnowheel
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


# http://trevorius.com/scrapbook/python/pyqt-multiple-inheritance/
from pypelyne2.src.modules.ui import pixmapdraggable


# class QWidgetOutput(QtGui.QWidget):
#     def __init__(self, output_object=None):
#         super(QWidgetOutput, self).__init__()
#
#         self.output = output_object
#
#         self.palette = QtGui.QPalette()
#
#     def set_palette(self):
#         self.palette.setColor(QtGui.QWidget().backgroundRole(), QtGui.QColor(50, 50, 50, 0))
#         self.ui.setPalette(self.palette)
#
#     def wheelEvent(self, event):
#         logging.info('wheelEvent on QWidgetOutput ({0})'.format(self))
#         event.ignore()
#
#
# class QWidgetTitle(QWidgetOutput):
#     def __init__(self, output_object=None):
#         super(QWidgetTitle, self).__init__()
#
#         self.output = output_object
#
#         self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
#                                           'src',
#                                           'modules',
#                                           'ui',
#                                           'output',
#                                           'output_widget.ui'))
#
#         self.set_palette()
#
#         self.ui.label_title.setText('hallo')


class Port(QtGui.QGraphicsItem):
    def __init__(self, node_object=None, output_object=None, port_id=None):
        super(Port, self).__init__()

        self.node_object = node_object

        self.uuid = port_id or str(uuid.uuid4())

        self.setAcceptsHoverEvents(True)

        # self.z = self.zValue()

        self.palette_temp = QtGui.QPalette()
        self.color_item = QtGui.QColor(255, 0, 0)

        self.output_object = output_object or parse_outputs.get_outputs()[random.randint(0, len(parse_outputs.get_outputs())-1)]

        self.hovered = False

        self.rect = QtCore.QRectF(-SETTINGS.OUTPUT_RADIUS/2,
                                  -SETTINGS.OUTPUT_RADIUS/2,
                                  SETTINGS.OUTPUT_RADIUS,
                                  SETTINGS.OUTPUT_RADIUS)

        # self.widget_title = QWidgetTitle()

        self.widget_title = None
        self.widget_title_proxy = None
        self.set_label()
        self.set_color()

    def set_palette_temp(self):
        self.palette_temp.setColor(QtGui.QWidget().backgroundRole(), QtGui.QColor(50, 50, 50, 0))
        if SETTINGS.TRANSPARENT_OUTPUT_LABEL:
            self.widget_title.setPalette(self.palette_temp)

    def set_color(self):
        self.color_item.setNamedColor(self.output_object.color)

    def boundingRect(self):
        return self.rect

    def set_label(self):
        self.widget_title = QtGui.QLabel(str(self.output_object.abbreviation + ' ' + self.uuid))

        # self.widget_title.setVisible(False)
        self.set_palette_temp()
        self.widget_title_proxy = qgraphicsproxywidgetnowheel.QGraphicsProxyWidgetNoWheel()

        self.widget_title_proxy.setWidget(self.widget_title)
        self.widget_title_proxy.setParentItem(self)

        self.widget_title.setVisible(SETTINGS.DISPLAY_OUTPUT_NAME)

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

        self.drag_cursor = QtGui.QCursor(QtCore.Qt.OpenHandCursor)

        self.set_label_pos()

        # print self.z
        # print self.zValue()

    def set_label_pos(self):
        self.widget_title_proxy.setPos(-self.widget_title_proxy.rect().width()-SETTINGS.OUTPUT_RADIUS/2-SETTINGS.OUTPUT_SPACING,
                                       -self.widget_title_proxy.rect().height()/2)

    def hoverEnterEvent(self, event):
        logging.info('hoverEnterEvent on Output ({0})'.format(self))

        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

        self.widget_title.setVisible(True)
        # self.widget_title_proxy.setZValue(500)

        self.hovered = True

        return QtGui.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        logging.info('hoverLeaveEvent on Output ({0})'.format(self))

        QtGui.QApplication.restoreOverrideCursor()
        # self.widget_title_proxy.setZValue(self.z)

        self.widget_title.setVisible(SETTINGS.DISPLAY_OUTPUT_NAME)

        self.hovered = False

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

        pixmap = compositeicon.CompositeIconOutput(self.output_object).output_icon

        icon.setPixmap(pixmap)

        drag = QtGui.QDrag(icon)
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap)
        # drag.setHotSpot(event.pos())

        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            pass
        #     print 'moved'
        # else:
        #     print 'copied'

        return QtGui.QGraphicsItem.mouseMoveEvent(self, event)

    def dropEvent(self, event):
        logging.info('dropEvent on {0}'.format(self))


class Input(Port):
    def __init__(self, node_object=None, output_object=None, port_id=None):
        super(Input, self).__init__(node_object, output_object, port_id)

        self.set_label_pos()

    def set_label_pos(self):
        self.widget_title_proxy.setPos(SETTINGS.OUTPUT_RADIUS/2+SETTINGS.OUTPUT_SPACING,
                                       -self.widget_title_proxy.rect().height()/2)

    def hoverEnterEvent(self, event):
        logging.info('hoverEnterEvent on Input ({0})'.format(self))

        # QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        # self.widget_title_proxy.setZValue(500)
        self.widget_title.setVisible(True)

        # print 'there'

        self.hovered = True

        return QtGui.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        logging.info('hoverLeaveEvent on Input ({0})'.format(self))

        # QtGui.QApplication.restoreOverrideCursor()

        # self.widget_title_proxy.setZValue(self.z)

        self.widget_title.setVisible(SETTINGS.DISPLAY_OUTPUT_NAME)

        # print 'here'

        self.hovered = False

        return QtGui.QGraphicsItem.hoverLeaveEvent(self, event)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on Input ({0})'.format(self))

    def mouseMoveEvent(self, event):
        logging.info('mouseMoveEvent on Input {0}'.format(self))
