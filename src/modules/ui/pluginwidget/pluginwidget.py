import os
import PyQt4.QtGui as QtGui
import PyQt4.uic as uic
import src.conf.settings.SETTINGS as SETTINGS
import src.modules.ui.pixmapdraggable.pixmapdraggable as pixmapdraggable


class PluginWidget(QtGui.QWidget):
    def __init__(self, plugin=None, mainwindow=None):
        super(PluginWidget, self).__init__()

        self.mainwindow = mainwindow

        self.processes = []

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'pluginwidget',
                                          'pluginwidget.ui'), self)

        if plugin.icon is None:
            self.icon = QtGui.QPixmap(SETTINGS.PLUGINS_DEFAULT_ICON).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)
        else:
            self.icon = QtGui.QPixmap(os.path.join(SETTINGS.PLUGINS_ICONS,
                                                   plugin.icon)).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        self.pixmap_x32 = pixmapdraggable.PixmapDraggable(plugin.x32, self.mainwindow)
        self.pixmap_x64 = pixmapdraggable.PixmapDraggable(plugin.x64, self.mainwindow)

        self.pixmap_x32.setToolTip('{0} {1} {2} is not available'.format(plugin.family,
                                                                         plugin.release_number,
                                                                         'x32'))
        self.pixmap_x64.setToolTip('{0} {1} {2} is not available'.format(plugin.family,
                                                                         plugin.release_number,
                                                                         'x64'))

        self.ui.label.setText('{0} {1}'.format(plugin.family, plugin.release_number))
        self.ui.label.setEnabled(False)

        self.ui.pixmaps_layout.addWidget(self.pixmap_x32)
        self.ui.pixmaps_layout.addWidget(self.pixmap_x64)

        self.pixmap_x32.setEnabled(False)
        self.pixmap_x64.setEnabled(False)

        if SETTINGS.DISPLAY_X32 and plugin.executable_x32 is not None:
            self.pixmap_x32.setEnabled(True)
            self.pixmap_x32.setToolTip('double click to launch. '
                                       'drag to create {0} {1} {2} node.'.format(plugin.family,
                                                                                 plugin.release_number,
                                                                                 plugin.architecture))

            self.ui.label.setEnabled(True)

        if SETTINGS.DISPLAY_X64 and plugin.executable_x64 is not None:
            self.pixmap_x64.setEnabled(True)
            self.pixmap_x64.setToolTip('double click to launch. '
                                       'drag to create {0} {1} {2} node.'.format(plugin.family,
                                                                                 plugin.release_number,
                                                                                 plugin.architecture))

            self.ui.label.setEnabled(True)


class FarmWidget(PluginWidget):
    def __init__(self):
        super(FarmWidget, self).__init__()
