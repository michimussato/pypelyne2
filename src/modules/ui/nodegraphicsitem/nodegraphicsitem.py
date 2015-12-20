import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import src.conf.settings.SETTINGS as SETTINGS
import src.modules.ui.compositeicon.compositeicon as compositeicon
import src.parser.parse_tasks as parse_tasks
# import os


class NodeGraphicsItem(QtGui.QGraphicsItem):
    def __init__(self, position, plugin):
        super(NodeGraphicsItem, self).__init__()

        # self.setParentItem(parent)

        # self.scene = scene

        self.plugin = plugin
        self.compositor = compositeicon.CompositeIcon(self.plugin)

        self.rect = QtCore.QRectF(0, 0, 200, 40)
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        # self.setFlag(self.ItemIsSelectable, True)
        # self.setFlag(self.ItemIsMovable, True)
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

        # self.label = None
        self.label = QtGui.QGraphicsTextItem()
        # self.label_bounding_rect = 0



        self.task_color = '#FF00FF'
        self.set_task_color()
        self.set_label(self.plugin.label)

        self.icon = None
        self.arch_icon = None
        self.lock_icon = None
        self.maximize_icon = None
        self.preview_icon = None
        self.set_task_icon()
        self.set_arch_icon()
        self.set_lock_icon()
        self.set_maximize_icon()
        self.set_preview_icon()

        # self.installSceneEventFilter(self)

        self.task_menu = QtGui.QComboBox()
        self.task_menu_proxy = QtGui.QGraphicsProxyWidget()
        # self.setVisible(False)
        self.add_task_menu()

        self.status_menu = QtGui.QComboBox()
        self.status_menu_proxy = QtGui.QGraphicsProxyWidget()
        self.add_status_menu()

    # def eventFilter(self, source, event):
    #     if event.type() == QtCore.QEvent.MouseMove and source is self.scene():
    #         pos = event.pos()
    #         print('mouse move: (%d, %d)' % (pos.x(), pos.y()))
    #     return QtGui.QWidget.eventFilter(self, source, event)

    # def mouseMoveEvent(self, event):
    #     print event
    #     # event_pos_scene = event.pos()
    #     # previous_pos = self.mouse_position_previous
    #     # delta = previous_pos - event_pos_scene
    #     #
    #     # mouse_modifiers = QtGui.QApplication.mouseButtons()
    #     # keyboard_modifiers = QtGui.QApplication.keyboardModifiers()
    #     # if mouse_modifiers == QtCore.Qt.MidButton \
    #     #         or keyboard_modifiers == QtCore.Qt.ControlModifier and mouse_modifiers == QtCore.Qt.LeftButton:
    #     #     group = self.scene.createItemGroup(self.scene.node_items)
    #     #     self.point.setPos(event_pos_scene)
    #     #     group.translate(-1*delta.x(), -1*delta.y())
    #     #     self.scene.destroyItemGroup(group)
    #     #
    #     # # else:
    #     # #     event.ignore()
    #     #
    #     # self.mouse_position_previous = event_pos_scene
    #
    # # def mouseDoubleClickEvent(self, event):
    # #     print event

    def set_preview_icon(self):
        # TODO: proper alignment
        import random
        import os
        img = os.path.join(SETTINGS.ICONS_DIR, 'rand_img', random.choice(SETTINGS.ICON_PREVIEW_PLACEHOLDER))
        print img
        img_pixmap = QtGui.QPixmap(img)
        if img_pixmap.width() > img_pixmap.height():
            # print 'wide'
            img_pixmap = img_pixmap.scaledToWidth(SETTINGS.PLUGINS_ICON_HEIGHT*2, QtCore.Qt.SmoothTransformation)
        else:
            # print 'long'
            img_pixmap = img_pixmap.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT*2, QtCore.Qt.SmoothTransformation)
        self.preview_icon = QtGui.QGraphicsPixmapItem(img_pixmap)
        self.preview_icon.setParentItem(self)
        self.preview_icon.setScale(SETTINGS.ICON_SCALE)
        print self.preview_icon.boundingRect()

    def set_label(self, text):
        # self.setData(0, text)

        self.label.setPlainText(text)
        # self.label = text
        node_label_color = QtGui.QColor(255, 255, 255)
        node_label_color.setNamedColor(SETTINGS.COLOR_LABEL)
        self.label.setDefaultTextColor(node_label_color)


        self.label.setParentItem(self)

        self.label_bounding_rect = self.label.boundingRect().width()

    def set_task_icon(self):
        self.icon = QtGui.QGraphicsPixmapItem(self.compositor.pixmap_no_overlay)

        self.icon.setParentItem(self)
        self.icon.setScale(SETTINGS.ICON_SCALE)

    def set_arch_icon(self):
        self.arch_icon = QtGui.QGraphicsPixmapItem(self.compositor.arch_icon)
        self.arch_icon.setParentItem(self)
        self.arch_icon.setScale(SETTINGS.ICON_SCALE)
        # print self.icon.boundingRect().width()

    def set_lock_icon(self):
        self.lock_icon = QtGui.QGraphicsPixmapItem(self.compositor.lock)
        self.lock_icon.setParentItem(self)
        self.lock_icon.setScale(SETTINGS.ICON_SCALE)

    def set_maximize_icon(self):
        self.maximize_icon = QtGui.QGraphicsPixmapItem(self.compositor.maximize)
        self.maximize_icon.setParentItem(self)
        self.maximize_icon.setScale(SETTINGS.ICON_SCALE)

    def add_task_menu(self):
        self.task_menu.addItem('-select task-')

        tasks = parse_tasks.get_tasks()

        for task in tasks:
            task_menu_item = self.task_menu.addItem(task.task)
            # task_menu_item.setItemData()

        self.task_menu_proxy.setWidget(self.task_menu)
        self.task_menu_proxy.setParentItem(self)

    def add_status_menu(self):
        self.status_menu.addItem('-select status-')

        states = ['waiting', 'in progress', 'whatever it might be']

        for status in states:
            task_menu_item = self.status_menu.addItem(status)
            # task_menu_item.setItemData()

        self.status_menu_proxy.setWidget(self.status_menu)
        self.status_menu_proxy.setParentItem(self)

    def boundingRect(self):
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsMovable, True)
        return self.rect

    def hoverEnterEvent(self, event):
        self.hovered = True
        # self.task_menu_proxy.setVisible(True)
        # self.task_menu.setVisible(True)
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
        # self.task_menu_proxy.setVisible(False)
        print 'leave'

    # def keyPressEvent(self, event):
    #     print 'hee'
    #     modifiers = QtGui.QApplication.keyboardModifiers()
    #     if self.hovered and modifiers == QtCore.Qt.ControlModifier:
    #         print 'disable'
    #         self.setFlag(self.ItemIsSelectable, False)
    #         self.setFlag(self.ItemIsMovable, False)

    def paint(self, painter, option, widget):

        proxy_width = self.task_menu_proxy.rect().width()

        # print self.task_menu_proxy.rect()
        # print dir(self.icon)

        # first row
        self.icon.setPos(QtCore.QPointF(0, 0))
        self.arch_icon.setPos(QtCore.QPointF(SETTINGS.ICON_SCALE*SETTINGS.PLUGINS_ICON_HEIGHT, 0))
        self.label.setPos(QtCore.QPointF((2*SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE, 0))
        self.lock_icon.setPos(QtCore.QPointF((2*SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE+self.label.boundingRect().width(), 0))
        self.maximize_icon.setPos(QtCore.QPointF(3*(SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE+self.label.boundingRect().width(), 0))

        # second row
        # TODO: proper alignment
        # self.preview_icon.setPos((((self.icon.boundingRect().width()+self.arch_icon.boundingRect().width())*(2*SETTINGS.ICON_SCALE))-(self.preview_icon.boundingRect().width()))*0.25, self.icon.boundingRect().height()*(2*SETTINGS.ICON_SCALE)+((self.task_menu_proxy.boundingRect().height()+self.status_menu_proxy.boundingRect().height())-self.preview_icon.boundingRect().height())*0.5)
        # self.preview_icon.setPos((((2*SETTINGS.PLUGINS_ICON_HEIGHT)*(2*SETTINGS.ICON_SCALE))-(self.preview_icon.boundingRect().width()))*0.25, ((SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE)+0.5*(SETTINGS.PLUGINS_ICON_HEIGHT-self.preview_icon.boundingRect().height()))

        if self.preview_icon.boundingRect().width() < self.preview_icon.boundingRect().height():
            # hochformat
            self.preview_icon.setPos((2*SETTINGS.PLUGINS_ICON_HEIGHT-self.preview_icon.boundingRect().width())*0.5*SETTINGS.ICON_SCALE, SETTINGS.PLUGINS_ICON_HEIGHT*SETTINGS.ICON_SCALE)
        elif self.preview_icon.boundingRect().width() == self.preview_icon.boundingRect().height():
            self.preview_icon.setPos(0, SETTINGS.PLUGINS_ICON_HEIGHT*SETTINGS.ICON_SCALE)
        else:
            # querformat
            self.preview_icon.setPos(0, (2*SETTINGS.PLUGINS_ICON_HEIGHT-self.preview_icon.boundingRect().height())*0.5*SETTINGS.ICON_SCALE+SETTINGS.PLUGINS_ICON_HEIGHT*SETTINGS.ICON_SCALE)

        # print self.task_menu_proxy.boundingRect().height()

        self.task_menu_proxy.setPos((2*SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE, self.label.boundingRect().height())
        self.status_menu_proxy.setPos((2*SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE, self.label.boundingRect().height()+self.task_menu_proxy.boundingRect().height())
        # self.task_menu_proxy.setPos(0, 0)

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

        self.rect.setWidth(max((4*SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE+self.label.boundingRect().width(),
                               (max(output_list_text_width) + 80) + (max(input_list_text_width))))

    def resize_height(self):
        # self.rect.setHeight(max([(len(self.inputs)+1)*20, (len(self.outputs)+1)*20])+(self.icon.boundingRect().height()+self.preview_icon.boundingRect().height()))
        self.rect.setHeight(max([self.label.boundingRect().height()+self.task_menu_proxy.boundingRect().height()+self.status_menu_proxy.boundingRect().height(), ((3*SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE)])+max([(len(self.inputs))*20, (len(self.outputs))*20]))
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
