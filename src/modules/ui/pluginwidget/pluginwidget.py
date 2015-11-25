import os

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

import src.conf.settings.SETTINGS as SETTINGS
import src.modules.launch.launch as launch


class PixmapDraggable(QtGui.QLabel):
    # http://stackoverflow.com/questions/5284648/init-method-for-subclass-of-pyqt-qtablewidgetitem
    def __init__(self, plugin, *args, **kwargs):
        super(PixmapDraggable, self).__init__(*args, **kwargs)

        # print dir(plugin)

        self.plugin = plugin

        self.setText('{} {}'.format(plugin.family, plugin.release_number))

        if plugin.icon is None:
            self.icon = QtGui.QPixmap(SETTINGS.PLUGINS_DEFAULT_ICON).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)
        else:
            self.icon = QtGui.QPixmap(os.path.join(SETTINGS.PLUGINS_ICONS,
                                                   plugin.icon)).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        self.pixmap = QtGui.QPixmap(SETTINGS.PLUGINS_ICON_HEIGHT, SETTINGS.PLUGINS_ICON_HEIGHT)

        if plugin.architecture == 'x32':
            self.arch_icon = QtGui.QPixmap(SETTINGS.ICON_X32).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT/2.5)
        elif plugin.architecture == 'x64':
            self.arch_icon = QtGui.QPixmap(SETTINGS.ICON_X64).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT/2.5)

        self.color = QtGui.QColor(0, 0, 0, 0)
        self.pixmap.fill(self.color)

        self.painter = QtGui.QPainter()
        self.painter.begin(self.pixmap)
        # http://doc.qt.io/qt-4.8/qpainter.html#CompositionMode-enum
        self.painter.setCompositionMode(self.painter.CompositionMode_SourceOver)
        self.painter.drawPixmap(0, 0, self.icon)
        self.painter.drawPixmap(0, 0, self.arch_icon)
        self.painter.end()

        self.setPixmap(self.pixmap)

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
        pixmap = QtGui.QPixmap(self.pixmap).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        # make a QDrag
        drag = QtGui.QDrag(self)
        # put our MimeData
        drag.setMimeData(mime_data)
        # set its Pixmap
        drag.setPixmap(pixmap)
        # shift the Pixmap so that it coincides with the cursor position
        drag.setHotSpot(e.pos())
        # print 'hello'

        # start the drag operation
        # exec_ will return the accepted action from dropEvent
        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            print 'moved'
        else:
            print 'copied'

    # def mouseDoubleClickEvent(self, event):
    #     print 'test'
    #
    # def mousePressEvent(self, event):
    #     return
    #     # self.setCursor(QtCore.Qt.BusyCursor)
    #
    # def mouseReleaseEvent(self, event):
    #     return
    #     # self.setCursor(QtCore.Qt.ArrowCursor)
    #
    # # def mouseReleaseEvent(self, event):
    # #     # self.setEnabled(False)
    # #     pass


class PluginWidget(QtGui.QWidget):
    def __init__(self, plugin=None):
        super(PluginWidget, self).__init__()

        self.processes = []

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'pluginwidget',
                                          'pluginwidget.ui'), self)

        # self.ui.label_icon.setText('')
        # self.ui.label_icon.setEnabled(False)

        if plugin.icon is None:
            self.icon = QtGui.QPixmap(SETTINGS.PLUGINS_DEFAULT_ICON).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)
        else:
            self.icon = QtGui.QPixmap(os.path.join(SETTINGS.PLUGINS_ICONS,
                                                   plugin.icon)).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        self.pixmap_x32 = PixmapDraggable(plugin.x32, 'pixmap_x32')
        self.pixmap_x64 = PixmapDraggable(plugin.x64, 'pixmap_x64')

        self.pixmap_x32.setToolTip('{} {} is not available'.format(plugin.family, plugin.release_number))
        self.pixmap_x64.setToolTip('{} {} is not available'.format(plugin.family, plugin.release_number))

        self.ui.label.setText('{} {}'.format(plugin.family, plugin.release_number))
        self.ui.label.setEnabled(False)

        self.ui.verticalLayout_2.addWidget(self.pixmap_x32)
        self.ui.verticalLayout_2.addWidget(self.pixmap_x64)

        self.pixmap_x32.setEnabled(False)
        self.pixmap_x64.setEnabled(False)

        if plugin.executable_x32 is not None:
            self.pixmap_x32.setEnabled(True)
            self.pixmap_x32.setToolTip('double click to launch. drag to create {} {} node.'.format(plugin.family, plugin.release_number))

            self.ui.label.setEnabled(True)

            # self.tool_button_x32.setText('')
            # self.tool_button_x32.setAutoRaise(True)
            # self.tool_button_x32.setEnabled(True)
            # self.tool_button_x32.setPopupMode(self.tool_button_x32.MenuButtonPopup)
            # self.tool_button_x32.setMenu(self.tool_button_x32_menu)
            # self.tool_button_x32.clicked.connect(lambda: self.launch_instance(plugin=x32_object))
            # self.tool_button_x32.setToolTip('launch 32 bits instance of {}'.format(x32_object.label))

        if plugin.executable_x64 is not None:
            self.pixmap_x64.setEnabled(True)
            self.pixmap_x64.setToolTip('double click to launch. drag to create {} {} node.'.format(plugin.family, plugin.release_number))

            self.ui.label.setEnabled(True)

            # self.ui.label_icon.setEnabled(True)

            # self.tool_button_x64_menu = QtGui.QMenu()
            # self.tool_button_x64_menu.addAction('launch instance',
            #                                     lambda: self.launch_instance(plugin=x64_object))
            #
            # self.tool_button_x64.setText('')
            # self.tool_button_x64.setAutoRaise(True)
            # self.tool_button_x64.setEnabled(True)
            # self.tool_button_x64.setPopupMode(self.tool_button_x64.MenuButtonPopup)
            # self.tool_button_x64.setMenu(self.tool_button_x64_menu)
            # self.tool_button_x64.clicked.connect(lambda: self.launch_instance(plugin=x64_object))
            # self.tool_button_x64.setToolTip('launch 64 bits instance of {}'.format(x64_object.label))

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
