import os
import uuid
import logging
import random
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import PyQt4.uic as uic
import pypelyne2.src.parser.parse_outputs as parse_outputs
import pypelyne2.src.modules.ui.qgraphicsproxywidgetnowheel.qgraphicsproxywidgetnowheel as qgraphicsproxywidgetnowheel
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


# http://trevorius.com/scrapbook/python/pyqt-multiple-inheritance/


class QWidgetOutput(QtGui.QWidget):
    def __init__(self, output_object=None):
        super(QWidgetOutput, self).__init__()

        self.output = output_object

        self.palette = QtGui.QPalette()

    def set_palette(self):
        self.palette.setColor(QtGui.QWidget().backgroundRole(), QtGui.QColor(50, 50, 50, 0))
        self.ui.setPalette(self.palette)

    def wheelEvent(self, event):
        logging.info('wheelEvent on QWidgetOutput ({0})'.format(self))
        event.ignore()


class QWidgetTitle(QWidgetOutput):
    def __init__(self, output_object=None):
        super(QWidgetTitle, self).__init__()

        self.output = output_object

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'output',
                                          'output_widget.ui'))

        self.set_palette()

        self.ui.label_title.setText('hallo')


class Output(QtGui.QGraphicsItem):
    def __init__(self, node_object=None, output_object=None, port_id=None):
        super(Output, self).__init__()

        self.node_object = node_object

        self.output_object = output_object or parse_outputs.get_outputs()[random.randint(0, len(parse_outputs.get_outputs())-1)]

        self.color_item = QtGui.QColor(255, 0, 0)

        self.uuid = port_id or str(uuid.uuid4())

        self.setAcceptsHoverEvents(True)

        self.widget_title = QWidgetTitle()

        self.palette_temp = QtGui.QPalette()

        self.widget_title = None
        self.widget_title_proxy = None
        self.set_label()
        self.set_color()

        self.hovered = False

        self.rect = QtCore.QRectF(-SETTINGS.OUTPUT_RADIUS/2,
                                  -SETTINGS.OUTPUT_RADIUS/2,
                                  SETTINGS.OUTPUT_RADIUS,
                                  SETTINGS.OUTPUT_RADIUS)

    def set_color(self):
        self.color_item.setNamedColor(self.output_object.color)

    def boundingRect(self):
        return self.rect

    def set_palette_temp(self):
        self.palette_temp.setColor(QtGui.QWidget().backgroundRole(), QtGui.QColor(50, 50, 50, 0))
        self.widget_title.setPalette(self.palette_temp)

    def set_label(self):
        self.widget_title = QtGui.QLabel(str(self.output_object.abbreviation + ' ' + self.uuid))
        # self.widget_title.setVisible(False)
        self.set_palette_temp()
        self.widget_title_proxy = qgraphicsproxywidgetnowheel.QGraphicsProxyWidgetNoWheel()
        self.widget_title_proxy.setWidget(self.widget_title)
        self.widget_title_proxy.setParentItem(self)

        self.widget_title_proxy.setPos(-self.widget_title_proxy.rect().width()-SETTINGS.OUTPUT_RADIUS/2-SETTINGS.OUTPUT_SPACING,
                                       -self.widget_title_proxy.rect().height()/2)

    def paint(self, painter, option, widget):
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(1)

        painter.setPen(pen)

        painter.setBrush(QtGui.QBrush(self.color_item))

        painter.drawEllipse(self.rect)

    def hoverEnterEvent(self, event):
        logging.info('hoverEnterEvent on Output ({0})'.format(self))
        self.widget_title.setVisible(True)

        self.hovered = True

        return QtGui.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        logging.info('hoverLeaveEvent on Output ({0})'.format(self))
        self.widget_title.setVisible(False)

        self.hovered = False

        return QtGui.QGraphicsItem.hoverLeaveEvent(self, event)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on Output ({0})'.format(self))
