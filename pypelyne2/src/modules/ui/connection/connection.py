# import os
import logging
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class Connection(QtGui.QGraphicsPathItem):
    def __init__(self, start_item=None, end_item=None, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)

        # TODO: apply global scale

        self.path_item = None
        self.path_color = None
        self.node_output = False
        self.my_start_item = start_item
        self.my_end_item = end_item
        self.my_color = QtCore.Qt.black
        self.setZValue(-1.0)

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)

        self.setActive(True)

        self.hovered = False

        self.qp = QtGui.QPainterPathStroker()
        self.qp.setWidth(10)
        self.qp.setCapStyle(QtCore.Qt.SquareCap)
        self.shape = self.qp.createStroke(self.get_connection())

        self.setPen(QtGui.QPen(self.my_color, 2))

        self.path_color_item = QtGui.QColor(0, 0, 0)

        self.set_connection_color()

    # def hoverEnterEvent(self, event):
    #     self.hovered = True
    #     self.my_start_item.hovered = True
    #     self.my_end_item.hovered = True
    #
    # def hoverLeaveEvent(self, event):
    #     self.hovered = False
    #     self.my_start_item.hovered = False
    #     self.my_end_item.hovered = False

    # def mouseMoveEvent(self, event):
    #     pass

    # def shape(self):
    #     return self.shape

    def paint(self, painter, option, widget):
        line = self.get_connection()

        pen = self.pen()
        pen.setWidth(2)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # if not os.path.isdir(self.start_item_live_dir):
        #     pen.setStyle(QtCore.Qt.CustomDashLine)
        #     pen.setDashPattern([1, 4])
        #
        # else:
        #     pen.setStyle(QtCore.Qt.SolidLine)
        #
        # if self.hovered:
        #     pen.setWidth(3)
        #     self.setZValue(-1)
        #     pen.setColor(self.path_color_item.lighter(150))
        #
        # else:
        self.setZValue(-2)
        pen.setColor(self.path_color_item)

        painter.setPen(pen)

        self.setPath(line)

        painter.drawPath(line)

    # def get_end_item(self):
    #     return self.my_end_item
    #
    # def get_start_item(self):
    #     return self.my_start_item

    def get_connection(self):
        # print dir(self.my_start_item)
        p1 = QtCore.QPointF(self.my_start_item.sceneBoundingRect().center().x(), self.my_start_item.sceneBoundingRect().center().y())
        p2 = None
        p3 = None
        p4 = QtCore.QPointF(self.my_end_item.sceneBoundingRect().center().x(), self.my_end_item.sceneBoundingRect().center().y())
        p5 = None
        p6 = p4

        path = QtGui.QPainterPath(p1)

        if SETTINGS.LINE_TYPE == 'BEZIER' or SETTINGS.LINE_TYPE == 'EDGED':

            if SETTINGS.LINE_TYPE == 'BEZIER':

                if (p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD) < p4.x():
                    p2 = QtCore.QPointF((p4.x() + p1.x()) / 2 + SETTINGS.LINE_SWITCH_THRESHOLD, p1.y())
                    p3 = QtCore.QPointF((p4.x() + p1.x()) / 2 - SETTINGS.LINE_SWITCH_THRESHOLD, p4.y())

                    # print p2.x()
                    # if p2.x() <= SETTINGS.LINE_SWITCH_THRESHOLD:
                    #     p2.setX(SETTINGS.LINE_SWITCH_THRESHOLD)
                    #
                    # if p3.x() <= SETTINGS.LINE_SWITCH_THRESHOLD:
                    #     p3.setX(SETTINGS.LINE_SWITCH_THRESHOLD)

                elif (p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD) >= p4.x():
                    p2 = QtCore.QPointF(p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD*2, p1.y())
                    p3 = QtCore.QPointF(p4.x() - SETTINGS.LINE_SWITCH_THRESHOLD*2, p4.y())

                path.cubicTo(p2, p3, p4)

            elif SETTINGS.LINE_TYPE == 'EDGED':

                if (p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD) < p4.x():
                    p2 = QtCore.QPointF((p4.x() - p1.x()) / 2 + p1.x(), p1.y())
                    p3 = QtCore.QPointF((p4.x() - p1.x()) / 2 + p1.x(), p4.y())

                    path.lineTo(p2)

                    path2 = QtGui.QPainterPath(p2)
                    path2.lineTo(p3)

                    path3 = QtGui.QPainterPath(p3)
                    path3.lineTo(p4)

                    path.connectPath(path2)
                    path.connectPath(path3)

                elif (p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD) >= p4.x():

                    p2 = QtCore.QPointF(p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD/2, p1.y())
                    p3 = QtCore.QPointF(p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD/2, (p1.y() + p6.y())/2)
                    p4 = QtCore.QPointF(p6.x() - SETTINGS.LINE_SWITCH_THRESHOLD/2, (p1.y() + p6.y())/2)
                    p5 = QtCore.QPointF(p6.x() - SETTINGS.LINE_SWITCH_THRESHOLD/2, p6.y())

                    path.lineTo(p2)

                    path2 = QtGui.QPainterPath(p2)
                    path2.lineTo(p3)

                    path3 = QtGui.QPainterPath(p3)
                    path3.lineTo(p4)

                    path4 = QtGui.QPainterPath(p4)
                    path4.lineTo(p5)

                    path5 = QtGui.QPainterPath(p5)
                    path5.lineTo(p6)

                    path.connectPath(path2)
                    path.connectPath(path3)
                    path.connectPath(path4)
                    path.connectPath(path5)

        elif SETTINGS.LINE_TYPE == 'STRAIGHT':
            path.lineTo(p4)

        self.shape = self.qp.createStroke(path)

        return path

    def set_connection_color(self):
        self.path_color_item.setNamedColor(self.my_start_item.output_object.color)
