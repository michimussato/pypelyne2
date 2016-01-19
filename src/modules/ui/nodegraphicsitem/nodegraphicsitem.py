import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import logging
import src.conf.settings.SETTINGS as SETTINGS
import src.modules.ui.compositeicon.compositeicon as compositeicon
import src.parser.parse_tasks as parse_tasks


class QLabelCollapseExpand(QtGui.QLabel):
    def __init__(self):
        super(QLabelCollapseExpand, self).__init__()

    def mousePressEvent(self, event):
        self.emit(QtCore.SIGNAL('clicked'))


class QWidgetNode(QtGui.QWidget):
    def __init__(self):
        super(QWidgetNode, self).__init__()

        self.ui = None

        self.palette = QtGui.QPalette()

    def set_palette(self):
        self.palette.setColor(QtGui.QWidget().backgroundRole(), QtGui.QColor(50, 50, 50, 0))
        self.ui.setPalette(self.palette)

    def wheelEvent(self, event):
        event.ignore()


class QWidgetTitle(QWidgetNode):
    def __init__(self):
        super(QWidgetTitle, self).__init__()

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'nodegraphicsitem',
                                          'nodegraphicsitem_widget_title.ui'), self)

        self.set_palette()

        self.ui.label_lock_icon.setText('')

        self.setup_title()
        self.ui.label_title_edit.returnPressed.connect(self.update_title)

    def setup_title(self):
        self.ui.label_title.setToolTip('shift click to change name')
        self.ui.label_title.setText('no name')
        self.ui.label_title_edit.setToolTip('enter to submit')
        self.ui.label_title_edit.setText(self.ui.label_title.text())

        self.ui.label_title.setVisible(True)
        self.ui.label_title_edit.setVisible(False)

    def update_title(self):
        new_title = self.ui.label_title_edit.text()
        self.ui.label_title_edit.setText(self.ui.label_title_edit.text())
        self.ui.label_title.setText(new_title)
        self.ui.label_title.setVisible(True)
        self.ui.label_title_edit.setVisible(False)

    def mousePressEvent(self, event):
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()

        if keyboard_modifiers == QtCore.Qt.ShiftModifier:
            self.ui.label_title.setVisible(False)
            self.ui.label_title_edit.setVisible(True)

        return QWidgetNode.mouseMoveEvent(self, event)


class QWidgetElements(QWidgetNode):
    def __init__(self):
        super(QWidgetElements, self).__init__()

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'nodegraphicsitem',
                                          'nodegraphicsitem_widget_elements.ui'), self)

        self.set_palette()

    def mousePressEvent(self, event):
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()
        mouse_modifiers = QtGui.QApplication.mouseButtons()
        if mouse_modifiers == QtCore.Qt.MidButton \
                or keyboard_modifiers == QtCore.Qt.ControlModifier and mouse_modifiers == QtCore.Qt.LeftButton:
            event.ignore()
            return

        return QWidgetNode.mouseMoveEvent(self, event)


class QWidgetHeader(QWidgetNode):
    def __init__(self):
        super(QWidgetHeader, self).__init__()

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'nodegraphicsitem',
                                          'nodegraphicsitem_widget_header.ui'), self)

        self.set_palette()

        # self.ui.label_arch_icon.setText('')
        # self.ui.label_icon.setText('')
        # self.ui.label_label.setText('')


class QGraphicsProxyWidgetNoWheel(QtGui.QGraphicsProxyWidget):
    def __init__(self):
        super(QGraphicsProxyWidgetNoWheel, self).__init__()

    def wheelEvent(self, event):
        event.ignore()

    def mousePressEvent(self, event):
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()
        mouse_modifiers = QtGui.QApplication.mouseButtons()
        if mouse_modifiers == QtCore.Qt.MidButton \
                or keyboard_modifiers == QtCore.Qt.ControlModifier and mouse_modifiers == QtCore.Qt.LeftButton:
            event.ignore()
            return

        return QtGui.QGraphicsProxyWidget.mouseMoveEvent(self, event)


class NodeGraphicsItem(QtGui.QGraphicsItem):
    def __init__(self, position, plugin):
        super(NodeGraphicsItem, self).__init__()

        reload(SETTINGS)

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

        self.setPos(position)

        self.hovered = False
        self.output_list = []
        self.input_list = []
        self.outputs = []
        self.inputs = []

        # self.label = None
        self.label = QtGui.QGraphicsTextItem()
        # self.label = TitleTextItem()
        # self.label_bounding_rect = 0

        self.task_color_default = '#FFFFFF'
        self.task_color = None
        self.set_task_color()
        # self.set_label(self.plugin.abbreviation)

        self.widget_title = QWidgetTitle()
        self.widget_elements = QWidgetElements()
        # self.widget_header = QWidgetHeader()

        self.widget_title_proxy = QGraphicsProxyWidgetNoWheel()
        self.widget_elements_proxy = QGraphicsProxyWidgetNoWheel()
        # self.widget_header_proxy = QGraphicsProxyWidgetNoWheel()

        self.collapse = QLabelCollapseExpand()
        self.expand = QLabelCollapseExpand()

        self.icon = None
        self.arch_icon = None
        self.set_label(str(' '.join([self.plugin.family, self.plugin.release_number])))
        self.lock_icon = None
        self.maximize_icon = None
        # self.preview_icon = None
        self.set_task_icon()
        self.set_arch_icon()
        self.set_lock_icon()
        # self.set_maximize_icon()
        self.set_thumbnail_icon()

        # self.set_ui_icons()
        self.add_ui_elements()
        self.setup_expand_collapse()
        self.add_task_menu_items()
        self.add_status_menu_items()

        '''
        self.widget = QtGui.QWidget()

        self.layout = QtGui.QHBoxLayout()
        self.layout.addWidget(QtGui.QPushButton('1'))
        self.layout.addWidget(QtGui.QPushButton('2'))
        self.widget.setLayout(self.layout)
        self.widget_proxy = QtGui.QGraphicsProxyWidget()
        self.widget_proxy.setWidget(self.widget)
        self.widget_proxy.setParentItem(self)
        '''

    def setup_expand_collapse(self):

        self.collapse.setToolTip('collapse combo boxes')
        self.expand.setToolTip('expand combo boxes')

        self.widget_title.hlayout_expand_collapse.addWidget(self.collapse)
        self.widget_title.hlayout_expand_collapse.addWidget(self.expand)

        self.expand.setPixmap(self.compositor.expand_icon)
        self.collapse.setPixmap(self.compositor.collapse_icon)

        self.update_expand_collapse()

        self.expand.connect(self.expand, QtCore.SIGNAL('clicked'), self.collapse_layout)
        self.collapse.connect(self.collapse, QtCore.SIGNAL('clicked'), self.expand_layout)

    def update_expand_collapse(self):
        self.expand.setVisible(False)
        self.collapse.setVisible(False)

        self.expand.setVisible(bool(not self.widget_elements.widget_comboboxes.isVisible()))
        self.collapse.setVisible(bool(self.widget_elements.widget_comboboxes.isVisible()))

    def expand_layout(self):
        self.widget_elements.widget_comboboxes.setVisible(False)
        self.update_expand_collapse()
        # print self.widget_elements_proxy.boundingRect().width()
        self.resize()
        # print self.widget_elements_proxy.boundingRect().width()

    def collapse_layout(self):
        self.widget_elements.widget_comboboxes.setVisible(True)
        self.update_expand_collapse()
        # print self.widget_elements_proxy.boundingRect().width()
        self.resize()
        # print self.widget_elements_proxy.boundingRect().width()

    def set_thumbnail_icon(self):
        import random
        import os

        img = SETTINGS.ICON_THUMBNAIL_DEFAULT

        try:
            img = os.path.join(SETTINGS.ICONS_DIR, 'rand_img', random.choice(SETTINGS.ICON_THUMBNAIL_PLACEHOLDER))
        except IndexError, e:
            logging.info('no thumbnail for node found: {0}'.format(e))
        finally:
            if os.path.splitext(img)[1] not in SETTINGS.ICON_FORMATS:
                logging.info('bad thumbnail: {0}'.format(img))
                img = SETTINGS.ICON_THUMBNAIL_DEFAULT

        # if os.path.splitext(img)[1] == '.gif':
        #     img_pixmap = QtGui.QMovie(img)
        # else:
        img_pixmap = QtGui.QPixmap(img)

        if img_pixmap.width() > img_pixmap.height():
            logging.info('thumbnail has landscape format')
            img_pixmap = img_pixmap.scaledToWidth(SETTINGS.PLUGINS_ICON_HEIGHT*2, QtCore.Qt.SmoothTransformation)
        elif img_pixmap.width() == img_pixmap.height():
            logging.info('thumbnail has square format')
            img_pixmap = img_pixmap.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT*2, QtCore.Qt.SmoothTransformation)
        elif img_pixmap.width() < img_pixmap.height():
            logging.info('thumbnail has portrait format')
            img_pixmap = img_pixmap.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT*2, QtCore.Qt.SmoothTransformation)

        self.widget_title.preview_icon.setPixmap(img_pixmap)

        # self.preview_icon = QtGui.QGraphicsPixmapItem(img_pixmap)
        # self.preview_icon.setParentItem(self)
        # self.preview_icon.setScale(SETTINGS.ICON_SCALE)
        # print self.preview_icon.boundingRect()

    def set_label(self, text):
        # # self.setData(0, text)
        #
        # self.label.setPlainText(text)
        # # self.label = text
        # node_label_color = QtGui.QColor(255, 255, 255)
        # node_label_color.setNamedColor(SETTINGS.COLOR_LABEL)
        # self.label.setDefaultTextColor(node_label_color)
        #
        # self.label.setParentItem(self)

        # self.label_bounding_rect = self.label.boundingRect().width()

        # self.widget_header.label_label.setText('')
        self.widget_title.label_label.setText(text)

    def set_task_icon(self):
        # self.icon = QtGui.QGraphicsPixmapItem(self.compositor.pixmap_no_overlay)
        # self.icon.setParentItem(self)
        # self.icon.setScale(SETTINGS.ICON_SCALE)

        # self.widget_header.label_icon.setText('')
        self.widget_title.label_icon.setPixmap(self.compositor.pixmap_no_overlay.scaled(self.compositor.pixmap_no_overlay.size() * SETTINGS.ICON_SCALE))
        # print self.compositor.pixmap_no_overlay.size()
        # print type(self.compositor.pixmap_no_overlay)
        # print dir(self.compositor.pixmap_no_overlay)

    def set_arch_icon(self):
        # self.arch_icon = QtGui.QGraphicsPixmapItem(self.compositor.arch_icon)
        # self.arch_icon.setParentItem(self)
        # self.arch_icon.setScale(SETTINGS.ICON_SCALE)

        # print dir(self.compositor.arch_icon)

        # self.widget_header.label_arch_icon.setText('')
        self.widget_title.label_arch_icon.setPixmap(self.compositor.arch_icon.scaled(self.compositor.arch_icon.size() * SETTINGS.ICON_SCALE))

    def set_lock_icon(self):
        # self.lock_icon = QtGui.QGraphicsPixmapItem(self.compositor.lock)
        # self.lock_icon.setParentItem(self)
        # self.lock_icon.setScale(SETTINGS.ICON_SCALE)

        # self.widget_header.label_lock_icon.setText('')
        self.widget_title.label_lock_icon.setPixmap(self.compositor.lock.scaled(self.compositor.lock.size() * SETTINGS.ICON_SCALE))

    # def set_maximize_icon(self):
    #     # self.maximize_icon = QtGui.QGraphicsPixmapItem(self.compositor.maximize)
    #     # self.maximize_icon.setParentItem(self)
    #     # self.maximize_icon.setScale(SETTINGS.ICON_SCALE)
    #
    #     self.widget_header.label_maximize_icon.setPixmap(self.compositor.maximize.scaled(self.compositor.maximize.size() * SETTINGS.ICON_SCALE))

    def add_ui_elements(self):
        self.widget_title_proxy.setWidget(self.widget_title)
        self.widget_title_proxy.setParentItem(self)

        self.widget_elements_proxy.setWidget(self.widget_elements)
        self.widget_elements_proxy.setParentItem(self)

        self.widget_title_proxy.setWidget(self.widget_title)
        self.widget_title_proxy.setParentItem(self)

    def add_task_menu_items(self):
        combobox = self.widget_elements.combobox_task
        combobox.addItem('-select task-')

        index = 0

        tasks = parse_tasks.get_tasks()

        for task in tasks:
            index += 1
            # menu_item = QtGui.QAction()
            # menu_item.setText(task.task)
            # menu_item.setData(task)
            combobox.addItem(task.task)
            combobox.setItemData(index, task)

        combobox.activated.connect(self.change_task_color)

    def add_status_menu_items(self):
        combobox = self.widget_elements.combobox_status
        combobox.addItem('-select status-')

        states = ['waiting', 'in progress', 'whatever it might be', 'or even something very different']

        for status in states:
            combobox.addItem(status)

    def boundingRect(self):
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsMovable, True)
        return self.rect

    def hoverEnterEvent(self, event):
        self.hovered = True
        logging.info('enter event: {0}'.format(self))

        return QtGui.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        # self.icon.setScale(0.5)
        self.hovered = False
        # self.task_menu_proxy.setVisible(False)
        # print 'leave'
        logging.info('leave event: {0}'.format(self))

        return QtGui.QGraphicsItem.hoverLeaveEvent(self, event)

    def paint(self, painter, option, widget):

        # first row
        self.widget_title_proxy.setPos(0, 0)
        # self.icon.setPos(QtCore.QPointF(0, 0))
        # self.arch_icon.setPos(QtCore.QPointF(SETTINGS.ICON_SCALE * SETTINGS.PLUGINS_ICON_HEIGHT, 0))
        # self.label.setPos(QtCore.QPointF((2 *
        #                                  SETTINGS.PLUGINS_ICON_HEIGHT) *
        #                                  SETTINGS.ICON_SCALE,
        #                                  0))
        # # self.lock_icon.setPos(QtCore.QPointF((2 *
        # #                                      SETTINGS.PLUGINS_ICON_HEIGHT) *
        # #                                      SETTINGS.ICON_SCALE +
        # #                                      self.label.boundingRect().width(),
        # #                                      0))
        # self.lock_icon.setPos(QtCore.QPointF(self.rect.width() -
        #                                      SETTINGS.PLUGINS_ICON_HEIGHT *
        #                                      SETTINGS.ICON_SCALE *
        #                                      2,
        #                                      0))
        # # self.maximize_icon.setPos(QtCore.QPointF(3 *
        # #                                          SETTINGS.PLUGINS_ICON_HEIGHT *
        # #                                          SETTINGS.ICON_SCALE +
        # #                                          self.label.boundingRect().width(),
        # #                                          0))
        # self.maximize_icon.setPos(QtCore.QPointF(self.rect.width() -
        #                                          SETTINGS.PLUGINS_ICON_HEIGHT *
        #                                          SETTINGS.ICON_SCALE,
        #                                          0))

        # second row
        # self.widget_title_proxy.setPos(0, self.widget_header_proxy.boundingRect().height())
        # print self.widget_header_proxy.boundingRect()

        # third row
        self.widget_elements_proxy.setPos(0, self.widget_title_proxy.boundingRect().height())

        painter.setRenderHint(painter.Antialiasing)

        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        pen.setColor(QtCore.Qt.black)
        pen.setWidth(0)

        hover_color = QtGui.QColor(255, 160, 0)

        if option.state & QtGui.QStyle.State_Selected:
            # self.update_meta_task()
            self.setZValue(1)
            pen.setWidth(3)
            pen.setColor(hover_color)
            self.gradient.setColorAt(0, self.task_color_item)
            # self.gradient.setColorAt(1, self.application_color_item.darker(160))
            self.gradient.setColorAt(1, self.task_color_item)

            # if os.path.exists(os.path.join(self.location, 'locked')):
            #     self.gradient.setColorAt(0, self.task_color_item)
            #     self.gradient.setColorAt(1, QtCore.Qt.red)
            #
            # elif os.path.exists(os.path.join(self.location, 'checkedOut')):
            #     self.gradient.setColorAt(0, self.task_color_item)
            #     self.gradient.setColorAt(1, QtCore.Qt.white)

        elif option.state & QtGui.QStyle.State_MouseOver or self.hovered:
            pen.setWidth(2)
            self.setZValue(3)

            pen.setColor(hover_color)
            self.gradient.setColorAt(0, self.task_color_item)
            # self.gradient.setColorAt(1, self.application_color_item.darker(160))
            self.gradient.setColorAt(1, self.task_color_item.darker(160))

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
            # self.gradient.setColorAt(1, self.application_color_item.darker(160))
            self.gradient.setColorAt(1, self.task_color_item.darker(160))

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
            position = QtCore.QPointF(self.boundingRect().width() - output.rect.width(),
                                      (output.boundingRect().height() * (self.outputs.index(output) + 1)))
            output.setPos(position)

    def arrange_inputs(self):
        for input_item in self.inputs:
            position = QtCore.QPointF(0, ((self.inputs.index(input_item) + 1) * input_item.boundingRect().height()))
            input_item.setPos(position)

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

        # 4* SETTINGS.PLUGINS_ICON_HEIGHT * SETTINGS.ICON_SCALE + self.label.textWidth()
        # self.ui_elements_proxy.boundingRect().width()

        if self.widget_elements.widget_comboboxes.isVisible():
            self.rect.setWidth(max([
                                   max([self.widget_title_proxy.boundingRect().width(),
                                        self.widget_elements_proxy.boundingRect().width()]),
                                   (max(output_list_text_width) + 80) + (max(input_list_text_width))]))

        elif not self.widget_elements.widget_comboboxes.isVisible():
            # print self.widget_header_proxy.boundingRect().width()
            # print self.widget_title_proxy.boundingRect().width()
            # print self.widget_elements_proxy.boundingRect().width()
            self.rect.setWidth(max([self.widget_title_proxy.boundingRect().width(), self.widget_elements_proxy.boundingRect().width()]))
            # self.rect.setWidth(max([4*SETTINGS.PLUGINS_ICON_HEIGHT *
            #                        SETTINGS.ICON_SCALE +
            #                        max([self.label.boundingRect().width(),
            #                             self.widget_title_proxy.boundingRect().width()]),
            #                        (max(output_list_text_width) + 80) + (max(input_list_text_width))]))

    def resize_height(self):
        if self.widget_elements.widget_comboboxes.isVisible():
            self.rect.setHeight(max([self.widget_title_proxy.boundingRect().height() +
                                     self.widget_elements_proxy.boundingRect().height(),
                                     ((3*SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE)]) +
                                max([(len(self.inputs))*20,
                                     (len(self.outputs))*20]))

        elif not self.widget_elements.widget_comboboxes.isVisible():
            self.rect.setHeight(max([self.label.boundingRect().height() +
                                     self.widget_title_proxy.boundingRect().height(),
                                     ((3*SETTINGS.PLUGINS_ICON_HEIGHT)*SETTINGS.ICON_SCALE)]) +
                                max([(len(self.inputs))*20,
                                     (len(self.outputs))*20]))

        self.gradient = QtGui.QLinearGradient(self.rect.topLeft(), self.rect.bottomLeft())

    @property
    def current_task_type(self):
        return self.widget_elements.combobox_task.currentIndex()

    def change_task_color(self):
        combobox = self.widget_elements.combobox_task
        index = self.current_task_type

        # palette = QtGui.QPalette()

        if index == 0:

            # color = QtGui.QColor()

            self.task_color = self.task_color_default
            self.set_task_color()

            # print self.task_color_item.getRgb()

            # print dir(self.ui_elements)
        else:
            task_data = combobox.itemData(index).toPyObject()
            self.task_color = task_data.color
            self.set_task_color()

    def set_task_color(self):
        # self.task_color = self.task_menu.itemData(self.task_menu.currentIndex())
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

        task_color = self.task_color or self.task_color_default

        self.task_color_item.setNamedColor(task_color)

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
