import os

import PyQt4.QtGui as QtGui
# import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

import src.conf.settings.SETTINGS as SETTINGS


class PixmapClickable(QtGui.QPixmap, QtGui.QWidget):
    def __init__(self, *__args):
        super(PixmapClickable, self).__init__()
        # pass

    def mouseDoubleClickEvent(self, event):
        print 'test'

    # http://www.qtforum.org/article/34120/adding-a-clickable-image-to-a-window.html


class PluginWidget(QtGui.QWidget):
    def __init__(self, plugin=None):
        super(PluginWidget, self).__init__()

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT, 'src', 'modules', 'ui', 'pluginwidget', 'pluginwidget.ui'), self)

        self.ui.label_icon_x32.setText('')
        self.ui.label_icon_x64.setText('')

        if plugin.icon is None:
            self.icon = QtGui.QPixmap(SETTINGS.PLUGINS_DEFAULT_ICON).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)
        else:
            self.icon = QtGui.QPixmap(os.path.join(SETTINGS.PLUGINS_ICONS, plugin.icon)).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        self.ui.label.setText(' '.join([plugin.family, plugin.release_number]))
        self.ui.label_icon_x32.setPixmap(self.icon)
        self.ui.label_icon_x64.setPixmap(self.icon)
        self.ui.label_icon_x32.setEnabled(False)
        self.ui.label_icon_x64.setEnabled(False)

        if plugin.executable_x32 is not None:
            self.ui.label_icon_x32.setPixmap(self.icon)
            self.ui.label_icon_x32.setEnabled(True)

        if plugin.executable_x64 is not None:
            self.ui.label_icon_x64.setPixmap(self.icon)
            self.ui.label_icon_x64.setEnabled(True)
