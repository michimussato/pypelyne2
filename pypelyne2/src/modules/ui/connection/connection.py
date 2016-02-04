import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class Connection(QtGui.QGraphicsPathItem):
    def __init__(self, start_item=None, end_item=None, scene_object=None, *args, **kwargs):
        super(Connection, self).__init__(*args, **kwargs)

        self.scene_object = scene_object

        self.path_item = None
        self.path_color = None
        self.node_output = False
        self.my_start_item = start_item
        self.my_end_item = end_item
        self.my_color = QtCore.Qt.black
        self.setZValue(-1.0)

        self.p1 = QtCore.QPointF(self.my_start_item.sceneBoundingRect().center().x(),
                                 self.my_start_item.sceneBoundingRect().center().y())
        self.p2 = None
        self.p3 = None
        self.p4 = QtCore.QPointF(self.my_end_item.sceneBoundingRect().center().x(),
                                 self.my_end_item.sceneBoundingRect().center().y())
        self.p5 = None
        self.p6 = self.p4

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

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.my_start_item.hovered = True
        self.my_end_item.hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.my_start_item.hovered = False
        self.my_end_item.hovered = False
        self.update()

    def paint(self, painter, option, widget):
        line = self.get_connection()

        pen = self.pen()
        pen.setWidth(SETTINGS.LINE_WIDTH*self.scene_object.global_scale)
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
        # self.setZValue(-2)

        if self.hovered:
            pen.setWidth(SETTINGS.LINE_WIDTH_HOVER*self.scene_object.global_scale)
            pen.setColor(self.path_color_item.lighter(SETTINGS.LIGHTER_AMOUNT))
            # self.setZValue(0)
            # print self.zValue()
        else:
            pen.setWidth(SETTINGS.LINE_WIDTH*self.scene_object.global_scale)
            pen.setColor(self.path_color_item)
            # self.setZValue(-1)

        painter.setPen(pen)

        self.setPath(line)

        painter.drawPath(line)

    def get_connection(self):
        # print dir(self.my_start_item)
        self.p1 = QtCore.QPointF(self.my_start_item.sceneBoundingRect().center().x(), self.my_start_item.sceneBoundingRect().center().y())
        # self.p2 = None
        # self.p3 = None
        self.p4 = QtCore.QPointF(self.my_end_item.sceneBoundingRect().center().x(), self.my_end_item.sceneBoundingRect().center().y())
        # self.p5 = None
        self.p6 = self.p4

        path = QtGui.QPainterPath(self.p1)

        if SETTINGS.LINE_TYPE == 'BEZIER' or SETTINGS.LINE_TYPE == 'EDGED':

            if SETTINGS.LINE_TYPE == 'BEZIER':

                if (self.p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD) < self.p4.x():
                    self.p2 = QtCore.QPointF((self.p4.x() + self.p1.x()) / 2 + SETTINGS.LINE_SWITCH_THRESHOLD*self.scene_object.global_scale, self.p1.y())
                    self.p3 = QtCore.QPointF((self.p4.x() + self.p1.x()) / 2 - SETTINGS.LINE_SWITCH_THRESHOLD*self.scene_object.global_scale, self.p4.y())

                elif (self.p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD) >= self.p4.x():
                    self.p2 = QtCore.QPointF(self.p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD*2*self.scene_object.global_scale, self.p1.y())
                    self.p3 = QtCore.QPointF(self.p4.x() - SETTINGS.LINE_SWITCH_THRESHOLD*2*self.scene_object.global_scale, self.p4.y())

                path.cubicTo(self.p2, self.p3, self.p4)

            elif SETTINGS.LINE_TYPE == 'EDGED':

                if (self.p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD*self.scene_object.global_scale) < self.p4.x():
                    self.p2 = QtCore.QPointF((self.p4.x() - self.p1.x()) / 2 + self.p1.x(), self.p1.y())
                    self.p3 = QtCore.QPointF((self.p4.x() - self.p1.x()) / 2 + self.p1.x(), self.p4.y())

                    path.lineTo(self.p2)

                    path2 = QtGui.QPainterPath(self.p2)
                    path2.lineTo(self.p3)

                    path3 = QtGui.QPainterPath(self.p3)
                    path3.lineTo(self.p4)

                    path.connectPath(path2)
                    path.connectPath(path3)

                elif (self.p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD) >= self.p4.x():

                    self.p2 = QtCore.QPointF(self.p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD/2*self.scene_object.global_scale, self.p1.y())
                    self.p3 = QtCore.QPointF(self.p1.x() + SETTINGS.LINE_SWITCH_THRESHOLD/2*self.scene_object.global_scale, (self.p1.y() + self.p6.y())/2)
                    self.p4 = QtCore.QPointF(self.p6.x() - SETTINGS.LINE_SWITCH_THRESHOLD/2*self.scene_object.global_scale, (self.p1.y() + self.p6.y())/2)
                    self.p5 = QtCore.QPointF(self.p6.x() - SETTINGS.LINE_SWITCH_THRESHOLD/2*self.scene_object.global_scale, self.p6.y())

                    path.lineTo(self.p2)

                    path2 = QtGui.QPainterPath(self.p2)
                    path2.lineTo(self.p3)

                    path3 = QtGui.QPainterPath(self.p3)
                    path3.lineTo(self.p4)

                    path4 = QtGui.QPainterPath(self.p4)
                    path4.lineTo(self.p5)

                    path5 = QtGui.QPainterPath(self.p5)
                    path5.lineTo(self.p6)

                    path.connectPath(path2)
                    path.connectPath(path3)
                    path.connectPath(path4)
                    path.connectPath(path5)

        elif SETTINGS.LINE_TYPE == 'STRAIGHT':
            path.lineTo(self.p4)

        self.shape = self.qp.createStroke(path)

        return path

    def set_connection_color(self):
        if hasattr(self.my_start_item, 'output_object'):
            self.path_color_item.setNamedColor(self.my_start_item.output_object.color)

    def shape(self):
        return self.shape
