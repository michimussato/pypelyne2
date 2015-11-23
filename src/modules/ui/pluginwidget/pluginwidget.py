import os
import subprocess

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

import src.conf.settings.SETTINGS as SETTINGS


class PixmapClickable(QtGui.QPixmap, QtGui.QWidget):
    def __init__(self, *__args):
        super(PixmapClickable, self).__init__()
        # pass

    def mouseDoubleClickEvent(self, event):
        print 'test'

    # http://www.qtforum.org/article/34120/adding-a-clickable-image-to-a-window.html


class ToolButtonClickable(QtGui.QToolButton):
    def __init__(self):
        super(ToolButtonClickable).__init__()

    def mouseReleaseEvent(self, event):
        pass


class PluginWidget(QtGui.QWidget):
    def __init__(self, plugin=None):
        super(PluginWidget, self).__init__()

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT, 'src', 'modules', 'ui', 'pluginwidget', 'pluginwidget.ui'), self)

        self.ui.label_icon.setText('')
        self.ui.label_icon.setEnabled(False)

        if plugin.icon is None:
            self.icon = QtGui.QPixmap(SETTINGS.PLUGINS_DEFAULT_ICON).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)
        else:
            self.icon = QtGui.QPixmap(os.path.join(SETTINGS.PLUGINS_ICONS, plugin.icon)).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        self.ui.label.setText('{} {}'.format(plugin.family, plugin.release_number))
        self.ui.label.setEnabled(False)

        self.ui.label_icon.setPixmap(self.icon)

        self.ui.label_icon.setEnabled(False)

        self.ui.tool_button_x32.setIcon(QtGui.QIcon(SETTINGS.ICON_X32))
        self.ui.tool_button_x64.setIcon(QtGui.QIcon(SETTINGS.ICON_X64))

        self.ui.tool_button_x32.setEnabled(False)
        self.ui.tool_button_x64.setEnabled(False)
        self.ui.tool_button_x32.setToolTip('32 bits instance of {} {} is not available'.format(plugin.family, plugin.release_number))
        self.ui.tool_button_x64.setToolTip('64 bits instance of {} {} is not available'.format(plugin.family, plugin.release_number))

        if plugin.executable_x32 is not None:
            self.ui.label.setEnabled(True)

            self.ui.label_icon.setEnabled(True)

            self.tool_button_x32_menu = QtGui.QMenu()
            self.tool_button_x32_menu.addAction('launch instance',
                                                                 lambda: self.launch_instance_x32(plugin=plugin))

            self.ui.tool_button_x32.setText('')
            self.ui.tool_button_x32.setAutoRaise(True)
            self.ui.tool_button_x32.setEnabled(True)
            self.ui.tool_button_x32.setPopupMode(self.ui.tool_button_x32.MenuButtonPopup)
            self.ui.tool_button_x32.setMenu(self.tool_button_x32_menu)
            self.ui.tool_button_x32.clicked.connect(lambda: self.launch_instance_x32(plugin=plugin))
            self.ui.tool_button_x32.setToolTip('launch 32 bits instance of {} {}'.format(plugin.family, plugin.release_number))

        if plugin.executable_x64 is not None:
            self.ui.label.setEnabled(True)

            self.ui.label_icon.setEnabled(True)

            self.tool_button_x64_menu = QtGui.QMenu()
            self.tool_button_x64_menu.addAction('launch instance',
                                                lambda: self.launch_instance_x64(plugin=plugin))

            self.ui.tool_button_x64.setText('')
            self.ui.tool_button_x64.setAutoRaise(True)
            self.ui.tool_button_x64.setEnabled(True)
            self.ui.tool_button_x64.setPopupMode(self.ui.tool_button_x64.MenuButtonPopup)
            self.ui.tool_button_x64.setMenu(self.tool_button_x64_menu)
            self.ui.tool_button_x64.clicked.connect(lambda: self.launch_instance_x64(plugin=plugin))
            self.ui.tool_button_x64.setToolTip('launch 64 bits instance of {} {}'.format(plugin.family, plugin.release_number))

    def launch_instance_x32(self, plugin=None):
        process = subprocess.Popen(plugin.executable_x32)

    def launch_instance_x64(self, plugin=None):
        process = subprocess.Popen(plugin.executable_x64)
