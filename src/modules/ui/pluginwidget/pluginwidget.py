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

        if plugin.type == 'submitter':
            # print plugin
            self.pixmap = pixmapdraggable.PixmapDragAndDrop(plugin.submitter, self.mainwindow)

            self.pixmap.setToolTip('{0} {1} is not available'.format(plugin.family,
                                                                     plugin.release_number))

            self.ui.label.setText('{0} {1}'.format(plugin.family, plugin.release_number))
            self.ui.label.setEnabled(False)

            self.ui.pixmaps_layout.addWidget(self.pixmap)

            self.pixmap.setEnabled(False)

            if plugin.executable is not None:
                self.pixmap.setEnabled(True)
                self.pixmap.setToolTip('drag to create {0} {1} node.'.format(plugin.family,
                                                                             plugin.release_number))

                self.ui.label.setEnabled(True)
            else:
                self.pixmap.setVisible(False)

        elif plugin.type == 'standalone':

            if plugin.nodeable:
                self.pixmap_x32 = pixmapdraggable.PixmapFullFeature(plugin.x32, self.mainwindow)
                self.pixmap_x64 = pixmapdraggable.PixmapFullFeature(plugin.x64, self.mainwindow)

            else:
                self.pixmap_x32 = pixmapdraggable.PixmapNodeableFalse(plugin.x32, self.mainwindow)
                self.pixmap_x64 = pixmapdraggable.PixmapNodeableFalse(plugin.x64, self.mainwindow)

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
                if plugin.nodeable:
                    self.pixmap_x32.setEnabled(True)
                    self.pixmap_x32.setToolTip('double click to launch. '
                                               'drag to create {0} {1} {2} node.'.format(plugin.family,
                                                                                         plugin.release_number,
                                                                                         plugin.architecture))
                else:
                    self.pixmap_x32.setEnabled(True)
                    self.pixmap_x32.setToolTip('double click to launch {0} {1} {2}.'.format(plugin.family,
                                                                                             plugin.release_number,
                                                                                             plugin.architecture))

                self.ui.label.setEnabled(True)
            elif SETTINGS.DISPLAY_X32 and plugin.executable_x32 is None:
                self.ui.label.setEnabled(True)
            else:
                self.pixmap_x32.setVisible(False)

            if SETTINGS.DISPLAY_X64 and plugin.executable_x64 is not None:
                if plugin.nodeable:
                    self.pixmap_x64.setEnabled(True)
                    self.pixmap_x64.setToolTip('double click to launch. '
                                               'drag to create {0} {1} {2} node.'.format(plugin.family,
                                                                                         plugin.release_number,
                                                                                         plugin.architecture))
                else:
                    self.pixmap_x64.setEnabled(True)
                    self.pixmap_x64.setToolTip('double click to launch {0} {1} {2}.'.format(plugin.family,
                                                                                             plugin.release_number,
                                                                                             plugin.architecture))

                self.ui.label.setEnabled(True)
            elif SETTINGS.DISPLAY_X64 and plugin.executable_x64 is None:
                self.ui.label.setEnabled(True)
            else:
                self.pixmap_x64.setVisible(False)


# class FarmWidget(PluginWidget):
#     def __init__(self):
#         super(FarmWidget, self).__init__()
