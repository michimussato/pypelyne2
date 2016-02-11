import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.modules.ui.pixmapdraggable.pixmapdraggable as pixmapdraggable


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

        self.ui.label.setEnabled(False)

        if plugin.icon is None:
            self.icon = QtGui.QPixmap(SETTINGS.PLUGINS_DEFAULT_ICON).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)
        else:
            self.icon = QtGui.QPixmap(os.path.join(SETTINGS.PLUGINS_ICONS,
                                                   plugin.icon)).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        if plugin.type == 'submitter':
            self.pixmap = pixmapdraggable.PixmapDragAndDrop(plugin.submitter, self.mainwindow)

            self.pixmap.setToolTip('{0} {1} is not available'.format(plugin.family,
                                                                     plugin.release_number))

            self.ui.label.setText('{0} {1}'.format(plugin.family, plugin.release_number))

            self.ui.pixmaps_layout.addWidget(self.pixmap)

            self.pixmap.setEnabled(False)

            if plugin.executable is not None:

                self.pixmap.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

                self.pixmap.setEnabled(True)
                self.pixmap.setToolTip('drag to create {0} {1} node.'.format(plugin.family,
                                                                             plugin.release_number))

                self.ui.label.setEnabled(True)

        elif plugin.type == 'standalone':
            if plugin.architecture_agnostic:
                if plugin.nodeable:
                    self.pixmap = pixmapdraggable.PixmapFullFeature(plugin.agnostic, self.mainwindow)

                else:
                    self.pixmap = pixmapdraggable.PixmapNodeableFalse(plugin.agnostic, self.mainwindow)

                self.pixmap.setToolTip('{0} {1} is not available'.format(plugin.family,
                                                                         plugin.release_number))

                self.ui.label.setText('{0} {1}'.format(plugin.family, plugin.release_number))

                self.ui.pixmaps_layout.addWidget(self.pixmap)

                self.pixmap.setEnabled(False)

                if plugin.executable is not None:

                    self.pixmap.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

                    if plugin.nodeable:
                        self.pixmap.setEnabled(True)
                        self.pixmap.setToolTip('double click to launch. '
                                               'drag to create {0} {1} node.'.format(plugin.family,
                                                                                     plugin.release_number))
                    else:
                        self.pixmap.setEnabled(True)
                        self.pixmap.setToolTip('double click to launch {0} {1}.'.format(plugin.family,
                                                                                        plugin.release_number))

                    self.ui.label.setEnabled(True)

            else:
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

                self.ui.pixmaps_layout.addWidget(self.pixmap_x32)
                self.ui.pixmaps_layout.addWidget(self.pixmap_x64)

                self.pixmap_x32.setEnabled(False)
                self.pixmap_x64.setEnabled(False)

                if SETTINGS.DISPLAY_X32:

                    plugin_x32 = plugin.x32

                    if plugin_x32.executable is not None:

                        self.pixmap_x32.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

                        if plugin.nodeable:

                            self.pixmap_x32.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

                            self.pixmap_x32.setEnabled(True)
                            # print plugin_x32.executable
                            # print dir(plugin_x32)
                            # print plugin_x32.architecture
                            self.pixmap_x32.setToolTip('double click to launch. '
                                                       'drag to create {0} {1} {2} node.'.format(plugin_x32.family,
                                                                                                 plugin_x32.release_number,
                                                                                                 plugin_x32.architecture))
                        else:

                            self.pixmap_x32.setEnabled(True)
                            self.pixmap_x32.setToolTip('double click to launch {0} {1} {2}.'.format(plugin_x32.family,
                                                                                                    plugin_x32.release_number,
                                                                                                    plugin_x32.architecture))

                        self.ui.label.setEnabled(True)
                    else:
                        self.ui.label.setEnabled(False)
                else:
                    self.pixmap_x32.setVisible(False)

                if SETTINGS.DISPLAY_X64:

                    plugin_x64 = plugin.x64

                    if plugin_x64.executable is not None:

                        self.pixmap_x64.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

                        if plugin.nodeable:

                            self.pixmap_x64.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

                            self.pixmap_x64.setEnabled(True)
                            self.pixmap_x64.setToolTip('double click to launch. '
                                                       'drag to create {0} {1} {2} node.'.format(plugin_x64.family,
                                                                                                 plugin_x64.release_number,
                                                                                                 plugin_x64.architecture))
                        else:

                            self.pixmap_x64.setEnabled(True)
                            self.pixmap_x64.setToolTip('double click to launch {0} {1} {2}.'.format(plugin_x64.family,
                                                                                                    plugin_x64.release_number,
                                                                                                    plugin_x64.architecture))

                        self.ui.label.setEnabled(True)
                    else:
                        self.ui.label.setEnabled(False)
                else:
                    self.pixmap_x64.setVisible(False)
