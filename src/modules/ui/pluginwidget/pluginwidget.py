import os

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

import src.conf.settings.SETTINGS as SETTINGS
import src.modules.launch.launch as launch


# class PixmapClickable(QtGui.QPixmap):
#     def __init__(self, *__args):
#         super(PixmapClickable, self).__init__()
#         # pass
#
#     def mouseDoubleClickEvent(self, event):
#         print 'test'
#
#     # http://www.qtforum.org/article/34120/adding-a-clickable-image-to-a-window.html


class ToolButtonDraggable(QtGui.QToolButton):
    def __init__(self, plugin=None):
        super(ToolButtonDraggable, self).__init__()

        self.plugin = plugin

    def mouseMoveEvent(self, e):
        # http://stackoverflow.com/questions/14395799/pyqt4-drag-and-drop
        # if e.buttons() != QtCore.Qt.RightButton:
        #     return

        # write the relative cursor position to mime data
        mime_data = QtCore.QMimeData()
        # simple string with 'x,y'
        mime_data.setText('%d,%d' % (e.x(), e.y()))

        # let's make it fancy. we'll show a "ghost" of the button as we drag
        # grab the button to a pixmap
        # print self.plugin.icon
        pixmap = QtGui.QPixmap(self.plugin.icon).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        # make a QDrag
        drag = QtGui.QDrag(self)
        # put our MimeData
        drag.setMimeData(mime_data)
        # set its Pixmap
        drag.setPixmap(pixmap)
        # shift the Pixmap so that it coincides with the cursor position
        drag.setHotSpot(e.pos())

        # start the drag operation
        # exec_ will return the accepted action from dropEvent
        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            print 'moved'
        else:
            print 'copied'


class PixmapDraggable(QtGui.QLabel):
    # http://stackoverflow.com/questions/5284648/init-method-for-subclass-of-pyqt-qtablewidgetitem
    def __init__(self, plugin=None, *args, **kwargs):
        super(PixmapDraggable, self).__init__(*args, **kwargs)

        self.plugin = plugin

        self.setText('{} {}'.format(plugin.family, plugin.release_number))

        if plugin.icon is None:
            self.icon = QtGui.QPixmap(SETTINGS.PLUGINS_DEFAULT_ICON).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)
        else:
            self.icon = QtGui.QPixmap(os.path.join(SETTINGS.PLUGINS_ICONS,
                                                   plugin.icon)).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        self.pixmap = QtGui.QPixmap()

        qicon = QtGui.QPixmap(self.icon)
        qarch = QtGui.QPixmap(SETTINGS.ICON_X32).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT/2.5)

        color = QtGui.QColor(0, 0, 0, 0)
        self.pixmap.fill(color)

        painter = QtGui.QPainter()
        painter.begin(self.pixmap)
        # http://doc.qt.io/qt-4.8/qpainter.html#CompositionMode-enum
        painter.setCompositionMode(painter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, qicon)
        painter.drawPixmap(0, 0, qarch)
        painter.end()

        self.setPixmap(self.icon)

    def mouseMoveEvent(self, e):
        # http://stackoverflow.com/questions/14395799/pyqt4-drag-and-drop
        # if e.buttons() != QtCore.Qt.RightButton:
        #     return

        # write the relative cursor position to mime data
        mime_data = QtCore.QMimeData()
        # simple string with 'x,y'
        mime_data.setText('%d,%d' % (e.x(), e.y()))

        # let's make it fancy. we'll show a "ghost" of the button as we drag
        # grab the button to a pixmap
        # print self.plugin.icon
        pixmap = QtGui.QPixmap(self.plugin.icon).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        # make a QDrag
        drag = QtGui.QDrag(self)
        # put our MimeData
        drag.setMimeData(mime_data)
        # set its Pixmap
        drag.setPixmap(pixmap)
        # shift the Pixmap so that it coincides with the cursor position
        drag.setHotSpot(e.pos())
        print 'hello'

        # start the drag operation
        # exec_ will return the accepted action from dropEvent
        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            print 'moved'
        else:
            print 'copied'

    def mouseDoubleClickEvent(self, event):
        print 'test'

    def mousePressEvent(self, event):
        return
        # self.setCursor(QtCore.Qt.BusyCursor)

    def mouseReleaseEvent(self, event):
        return
        # self.setCursor(QtCore.Qt.ArrowCursor)

    # def mouseReleaseEvent(self, event):
    #     # self.setEnabled(False)
    #     pass


class PluginWidget(QtGui.QWidget):
    def __init__(self, plugin=None):
        super(PluginWidget, self).__init__()

        self.processes = []

        # self.plugin_x32 = plugin.x32
        # self.plugin_x64 = plugin.x64

        # self.setAcceptDrops(True)

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'pluginwidget',
                                          'pluginwidget.ui'), self)

        self.tool_button_x32 = ToolButtonDraggable(plugin=plugin)
        self.tool_button_x64 = ToolButtonDraggable(plugin=plugin)
        self.v_spacer = QtGui.QSpacerItem(1, 1, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)

        self.tool_buttons_layout.addWidget(self.tool_button_x32)
        self.tool_buttons_layout.addWidget(self.tool_button_x64)
        self.tool_buttons_layout.addItem(self.v_spacer)

        self.ui.label_icon.setText('')
        self.ui.label_icon.setEnabled(False)

        if plugin.icon is None:
            self.icon = QtGui.QPixmap(SETTINGS.PLUGINS_DEFAULT_ICON).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)
        else:
            self.icon = QtGui.QPixmap(os.path.join(SETTINGS.PLUGINS_ICONS,
                                                   plugin.icon)).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        # paint architecture on top of the application icon
        # qicon = QtGui.QPixmap(self.icon)
        # qarch = QtGui.QPixmap(SETTINGS.ICON_X32).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT/2.5)

        pixmap = PixmapDraggable(plugin, 'test')
        # color = QtGui.QColor(0, 0, 0, 0)
        # pixmap.fill(color)
        #
        # painter = QtGui.QPainter()
        # painter.begin(pixmap)
        # # http://doc.qt.io/qt-4.8/qpainter.html#CompositionMode-enum
        # painter.setCompositionMode(painter.CompositionMode_SourceOver)
        # painter.drawPixmap(0, 0, qicon)
        # painter.drawPixmap(0, 0, qarch)
        # painter.end()



        self.ui.label.setText('{} {}'.format(plugin.family, plugin.release_number))
        self.ui.label.setEnabled(False)

        # self.ui.label_icon.setPixmap(pixmap)
        self.ui.verticalLayout_2.addWidget(pixmap)
        self.ui.label_icon.setEnabled(False)

        self.tool_button_x32.setIcon(QtGui.QIcon(SETTINGS.ICON_X32))
        self.tool_button_x64.setIcon(QtGui.QIcon(SETTINGS.ICON_X64))

        self.tool_button_x32.setEnabled(False)
        self.tool_button_x64.setEnabled(False)
        self.tool_button_x32.setToolTip('32 bits instance of {} {} is not available'.format(plugin.family,
                                                                                            plugin.release_number))
        self.tool_button_x64.setToolTip('64 bits instance of {} {} is not available'.format(plugin.family,
                                                                                            plugin.release_number))

        if plugin.executable_x32 is not None:
            x32_object = plugin.x32

            self.ui.label.setEnabled(True)

            self.ui.label_icon.setEnabled(True)

            self.tool_button_x32_menu = QtGui.QMenu()
            self.tool_button_x32_menu.addAction('launch instance',
                                                lambda: self.launch_instance(plugin=x32_object))

            self.tool_button_x32.setText('')
            self.tool_button_x32.setAutoRaise(True)
            self.tool_button_x32.setEnabled(True)
            self.tool_button_x32.setPopupMode(self.tool_button_x32.MenuButtonPopup)
            self.tool_button_x32.setMenu(self.tool_button_x32_menu)
            self.tool_button_x32.clicked.connect(lambda: self.launch_instance(plugin=x32_object))
            self.tool_button_x32.setToolTip('launch 32 bits instance of {}'.format(x32_object.label))

        if plugin.executable_x64 is not None:
            x64_object = plugin.x64
            # plugin_x64 = plugin.x64()

            self.ui.label.setEnabled(True)

            self.ui.label_icon.setEnabled(True)

            self.tool_button_x64_menu = QtGui.QMenu()
            self.tool_button_x64_menu.addAction('launch instance',
                                                lambda: self.launch_instance(plugin=x64_object))

            self.tool_button_x64.setText('')
            self.tool_button_x64.setAutoRaise(True)
            self.tool_button_x64.setEnabled(True)
            self.tool_button_x64.setPopupMode(self.tool_button_x64.MenuButtonPopup)
            self.tool_button_x64.setMenu(self.tool_button_x64_menu)
            self.tool_button_x64.clicked.connect(lambda: self.launch_instance(plugin=x64_object))
            self.tool_button_x64.setToolTip('launch 64 bits instance of {}'.format(x64_object.label))

    def launch_instance(self, plugin=None):
        # print plugin
        process = QtCore.QProcess(self)
        process.started.connect(lambda: self.started(plugin=plugin))
        process.finished.connect(lambda: self.finished(plugin=plugin))
        process.start(plugin.executable, plugin.flags)

    def started(self, plugin):
        print 'plugin {} started'.format(plugin.label)

    def finished(self, plugin):
        print 'plugin {} finished'.format(plugin.label)

    def dropEvent(self, event):
        print 'drop'
