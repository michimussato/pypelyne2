import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import src.conf.settings.SETTINGS as SETTINGS
import src.modules.ui.compositeicon.compositeicon as compositeicon
# import os


class NodeGraphicsItem(QtGui.QGraphicsItem):
    def __init__(self, position, plugin):
        super(NodeGraphicsItem, self).__init__()

        # self.scene = scene

        self.plugin = plugin
        self.compositor = compositeicon.CompositeIcon(self.plugin)

        self.rect = QtCore.QRectF(0, 0, 200, 40)
        # self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsMovable, True)
        self.gradient = QtGui.QLinearGradient(self.rect.topLeft(), self.rect.bottomLeft())

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)

        self.task_color_item = QtGui.QColor(0, 0, 0)
        self.application_color_item = QtGui.QColor(0, 0, 0)

        # print type(position)

        self.setPos(position)

        self.hovered = False
        self.output_list = []
        self.input_list = []
        self.outputs = []
        self.inputs = []

        self.label = None
        self.label_bounding_rect = 0

        self.task_color = '#FF00FF'
        self.set_task_color()
        self.set_label(self.plugin.label)

        self.icon = None
        self.set_icon()

        # self.add_button()

    # def mouseDoubleClickEvent(self, event):
    #     print event

    def set_label(self, text):
        # self.setData(0, text)
        node_label = QtGui.QGraphicsTextItem(text)
        self.label = text
        node_label_color = QtGui.QColor(255, 255, 255)
        node_label_color.setNamedColor(SETTINGS.COLOR_LABEL)
        node_label.setDefaultTextColor(node_label_color)
        node_label.setPos(QtCore.QPointF(25, 0))

        node_label.setParentItem(self)

        self.label_bounding_rect = node_label.boundingRect().width()

    def set_icon(self):

        # node_icon_pixmap = QtGui.QPixmap(SETTINGS.CAPTURE_ICON_START).scaledToHeight(SETTINGS.ICON_HEIGHT, QtCore.Qt.SmoothTransformation)
        # node_arch_pixmap = QtGui.QPixmap(SETTINGS.ICON_X64).scaledToHeight(SETTINGS.ICON_HEIGHT, QtCore.Qt.SmoothTransformation)

        self.icon = QtGui.QGraphicsPixmapItem(self.compositor.pixmap_no_arch)
        # self.icon.setVisible(False)
        # node_arch = QtGui.QGraphicsPixmapItem(node_arch_pixmap)

        # node_icon.setPos(QtCore.QPointF(0, -(node_icon.boundingRect().height()/2)))

        # node_arch.setPos(QtCore.QPointF(30, -22))

        self.icon.setParentItem(self)
        self.icon.setScale(SETTINGS.ICON_SCALE)
        # self.icon.setPos(QtCore.QPointF(0, -(self.icon.boundingRect().height())*SETTINGS.ICON_SCALE))
        self.icon.setPos(QtCore.QPointF(0, 0))
        # node_arch.setParentItem(self)

    def add_button(self):
        btn = QtGui.QPushButton(self.label)
        # self.seta

    def boundingRect(self):
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsMovable, True)
        return self.rect

    def hoverEnterEvent(self, event):
        self.hovered = True
        # self.icon.setScale(1)
        # modifiers = QtGui.QApplication.keyboardModifiers()
        # if modifiers == QtCore.Qt.ControlModifier:
        #     print 'disable'
        #     self.setFlag(self.ItemIsSelectable, False)
        #     self.setFlag(self.ItemIsMovable, False)
        print 'enter'

    def hoverLeaveEvent(self, event):
        # self.icon.setScale(0.5)
        self.hovered = False
        print 'leave'

    def keyPressEvent(self, event):
        print 'hee'
        modifiers = QtGui.QApplication.keyboardModifiers()
        if self.hovered and modifiers == QtCore.Qt.ControlModifier:
            print 'disable'
            self.setFlag(self.ItemIsSelectable, False)
            self.setFlag(self.ItemIsMovable, False)

    def paint(self, painter, option, widget):
        # print 'paint'
        # painter = QtGui.QPainter()
        painter.setRenderHint(painter.Antialiasing)

        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(0)

        if option.state & QtGui.QStyle.State_Selected:
            # self.update_meta_task()
            self.setZValue(1)
            pen.setWidth(2)
            pen.setColor(QtCore.Qt.green)
            self.gradient.setColorAt(0, self.task_color_item)
            self.gradient.setColorAt(1, self.application_color_item.darker(160))

            # if os.path.exists(os.path.join(self.location, 'locked')):
            #     self.gradient.setColorAt(0, self.task_color_item)
            #     self.gradient.setColorAt(1, QtCore.Qt.red)
            #
            # elif os.path.exists(os.path.join(self.location, 'checkedOut')):
            #     self.gradient.setColorAt(0, self.task_color_item)
            #     self.gradient.setColorAt(1, QtCore.Qt.white)

        elif option.state & QtGui.QStyle.State_MouseOver or self.hovered:
            pen.setWidth(5)
            pen.setColor(QtCore.Qt.yellow)
            self.gradient.setColorAt(0, self.task_color_item)
            self.gradient.setColorAt(1, self.application_color_item.darker(160))

            # if os.path.exists(os.path.join(self.location, 'locked')):
            #     self.gradient.setColorAt(0, self.task_color_item)
            #     self.gradient.setColorAt(1, QtCore.Qt.red)
            #
            # elif os.path.exists(os.path.join(self.location, 'checkedOut')):
            #     self.gradient.setColorAt(0, self.task_color_item)
            #     self.gradient.setColorAt(1, QtCore.Qt.white)

        # elif os.path.exists(os.path.join(self.location, 'locked')):
        #     self.gradient.setColorAt(0, self.task_color_item)
        #     self.gradient.setColorAt(1, QtCore.Qt.red)
        #
        # elif os.path.exists(os.path.join(self.location, 'checkedOut')):
        #     self.gradient.setColorAt(0, self.task_color_item)
        #     self.gradient.setColorAt(1, QtCore.Qt.white)

        else:
            pen.setWidth(0)
            self.setZValue(0)
            self.gradient.setColorAt(0, self.task_color_item)
            self.gradient.setColorAt(1, self.application_color_item.darker(160))

        painter.setBrush(self.gradient)

        painter.setPen(pen)

        painter.drawRoundedRect(self.rect, SETTINGS.NODE_ROUNDNESS, SETTINGS.NODE_ROUNDNESS)

        for i in self.output_list:
            i.setPos(self.boundingRect().width() - i.rect.width(), i.pos().y())

        self.rect.setWidth(self.rect.width())
        self.arrange_outputs()
        self.arrange_inputs()
        self.resize()

    def arrange_outputs(self):
        for output in self.outputs:
            position = QtCore.QPointF(self.boundingRect().width() - output.rect.width(), ((output.boundingRect().height() * (self.outputs.index(output) + 1))))
            output.setPos(position)

    def arrange_inputs(self):
        for input in self.inputs:
            position = QtCore.QPointF(0, ((self.inputs.index(input) + 1) * input.boundingRect().height()))
            input.setPos(position)

    def resize(self):
        self.resize_height()
        self.resize_width()

    def resize_width(self):
        output_list_text_width = [0]
        input_list_text_width = [0]

        for i in self.input_list:
            input_list_text_width.append(int(i.childrenBoundingRect().width()))

        for i in self.output_list:
            output_list_text_width.append(int(i.childrenBoundingRect().width()))

        self.rect.setWidth(max((self.label_bounding_rect + 40 + 20),
                               (max(output_list_text_width) + 80) + (max(input_list_text_width))))

    def resize_height(self):
        self.rect.setHeight(max(len(self.inputs) + 1, len(self.outputs) + 1) * 20)
        self.gradient = QtGui.QLinearGradient(self.rect.topLeft(), self.rect.bottomLeft())

    def set_task_color(self):
        # self.task_color = '#FF00FF'

        # if os.path.basename(self.location)[:7].startswith('LDR'):
        #     if os.path.basename(self.location)[:7].endswith('LIB'):
        #         self.task_color = '#00FF00'
        #     else:
        #         for tab in self.main_window.content_tabs:
        #             if os.path.basename(self.location)[:7].endswith(tab['abbreviation']):
        #                 self.task_color = tab['loader_color']
        #                 break
        #
        # elif os.path.basename(self.location)[:7].startswith('SVR'):
        #     for tab in self.main_window.content_tabs:
        #         if os.path.basename(self.location)[:7].endswith(tab['abbreviation']):
        #             self.task_color = tab['saver_color']
        #
        # else:
        #     for task in self.main_window._tasks:
        #         # print task[u'abbreviation']
        #         # print self.nodeTask
        #         if self.nodeTask == task[u'task']:
        #             logging.info('task color description for task %s found' % task[u'abbreviation'])
        #             self.task_color = task[u'color']
        #             break

        self.task_color_item.setNamedColor(self.task_color)

    # def add_text(self, text):
    #     # self.setData(0, text)
    #     node_label = QtGui.QGraphicsTextItem(text)
    #     self.label = text
    #     node_label_color = (QtGui.QColor(255, 255, 255))
    #     node_label_color.setNamedColor('#080808')
    #     node_label.setDefaultTextColor(node_label_color)
    #     node_label.setPos(QtCore.QPointF(25, 0))
    #     node_label.setParentItem(self)
    #     self.label_bounding_rect = node_label.boundingRect().width()
    #
    #     self.resize_width()
