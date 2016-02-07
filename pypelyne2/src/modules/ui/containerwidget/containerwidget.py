import os
import logging
import PyQt4.QtGui as QtGui
import PyQt4.uic as uic
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.modules.ui.pixmapdraggable.pixmapdraggable as pixmapdraggable


class ContainerWidget(QtGui.QWidget):
    def __init__(self, container=None, mainwindow=None):
        super(ContainerWidget, self).__init__()

        self.mainwindow = mainwindow

        self.container = container

        # self.processes = []

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'containerwidget',
                                          'containerwidget.ui'), self)

        if self.container.icon is None:
            self.icon = QtGui.QPixmap(SETTINGS.CONTAINERS_DEFAULT_ICON).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)
        else:
            self.icon = QtGui.QPixmap(self.container.icon).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        self.pixmap = pixmapdraggable.PixmapContainer(self.container, self.mainwindow)

        self.ui.label.setText('{0}'.format(self.container.type))
        self.ui.label.setEnabled(False)

        self.ui.pixmaps_layout.addWidget(self.pixmap)

        self.pixmap.setToolTip('drag me onto node to create a new {0} container'.format(self.container.type))

        # self.pixmap.setEnabled(False)

        # if output.executable is not None:
        #     self.pixmap.setEnabled(True)
        #     self.pixmap.setToolTip('drag to create {0} {1} node.'.format(output.family,
        #                                                                  output.release_number))

        self.ui.label.setEnabled(True)

        self.set_color_hint()

    def set_color_hint(self):
        logging.info('containerwidget.set_color_hint() ({0})'.format(self))

        lineedit = self.ui.lineedit_color

        color_value = self.container.color

        lineedit.setText(color_value)

        palette = QtGui.QPalette()
        color = QtGui.QColor(0, 0, 0, 255)
        color.setNamedColor(color_value)

        palette.setColor(QtGui.QPalette.Base, color)

        lineedit.setPalette(palette)

        # elif plugin.type == 'standalone':
        #     if plugin.architecture_agnostic:
        #         if plugin.nodeable:
        #             self.pixmap = pixmapdraggable.PixmapFullFeature(plugin.agnostic, self.mainwindow)
        #
        #         else:
        #             self.pixmap = pixmapdraggable.PixmapNodeableFalse(plugin.agnostic, self.mainwindow)
        #
        #         self.pixmap.setToolTip('{0} {1} is not available'.format(plugin.family,
        #                                                                  plugin.release_number))
        #
        #         self.ui.label.setText('{0} {1}'.format(plugin.family, plugin.release_number))
        #         self.ui.label.setEnabled(False)
        #
        #         self.ui.pixmaps_layout.addWidget(self.pixmap)
        #
        #         self.pixmap.setEnabled(False)
        #
        #         if plugin.executable is not None:
        #             if plugin.nodeable:
        #                 self.pixmap.setEnabled(True)
        #                 self.pixmap.setToolTip('double click to launch. '
        #                                        'drag to create {0} {1} node.'.format(plugin.family,
        #                                                                              plugin.release_number))
        #             else:
        #                 self.pixmap.setEnabled(True)
        #                 self.pixmap.setToolTip('double click to launch {0} {1}.'.format(plugin.family,
        #                                                                                 plugin.release_number))
        #
        #             self.ui.label.setEnabled(True)
        #
        #     else:
        #         if plugin.nodeable:
        #             self.pixmap_x32 = pixmapdraggable.PixmapFullFeature(plugin.x32, self.mainwindow)
        #             self.pixmap_x64 = pixmapdraggable.PixmapFullFeature(plugin.x64, self.mainwindow)
        #
        #         else:
        #             self.pixmap_x32 = pixmapdraggable.PixmapNodeableFalse(plugin.x32, self.mainwindow)
        #             self.pixmap_x64 = pixmapdraggable.PixmapNodeableFalse(plugin.x64, self.mainwindow)
        #
        #         self.pixmap_x32.setToolTip('{0} {1} {2} is not available'.format(plugin.family,
        #                                                                          plugin.release_number,
        #                                                                          'x32'))
        #         self.pixmap_x64.setToolTip('{0} {1} {2} is not available'.format(plugin.family,
        #                                                                          plugin.release_number,
        #                                                                          'x64'))
        #
        #         self.ui.label.setText('{0} {1}'.format(plugin.family, plugin.release_number))
        #         self.ui.label.setEnabled(False)
        #
        #         self.ui.pixmaps_layout.addWidget(self.pixmap_x32)
        #         self.ui.pixmaps_layout.addWidget(self.pixmap_x64)
        #
        #         self.pixmap_x32.setEnabled(False)
        #         self.pixmap_x64.setEnabled(False)
        #
        #         if SETTINGS.DISPLAY_X32:
        #             if plugin.executable_x32 is not None:
        #                 if plugin.nodeable:
        #                     self.pixmap_x32.setEnabled(True)
        #                     self.pixmap_x32.setToolTip('double click to launch. '
        #                                                'drag to create {0} {1} {2} node.'.format(plugin.family,
        #                                                                                          plugin.release_number,
        #                                                                                          plugin.architecture))
        #                 else:
        #                     self.pixmap_x32.setEnabled(True)
        #                     self.pixmap_x32.setToolTip('double click to launch {0} {1} {2}.'.format(plugin.family,
        #                                                                                             plugin.release_number,
        #                                                                                             plugin.architecture))
        #
        #                 self.ui.label.setEnabled(True)
        #             else:
        #                 self.ui.label.setEnabled(False)
        #         else:
        #             self.pixmap_x32.setVisible(False)
        #
        #         if SETTINGS.DISPLAY_X64:
        #             if plugin.executable_x64 is not None:
        #                 if plugin.nodeable:
        #                     self.pixmap_x64.setEnabled(True)
        #                     self.pixmap_x64.setToolTip('double click to launch. '
        #                                                'drag to create {0} {1} {2} node.'.format(plugin.family,
        #                                                                                          plugin.release_number,
        #                                                                                          plugin.architecture))
        #                 else:
        #                     self.pixmap_x64.setEnabled(True)
        #                     self.pixmap_x64.setToolTip('double click to launch {0} {1} {2}.'.format(plugin.family,
        #                                                                                             plugin.release_number,
        #                                                                                             plugin.architecture))
        #
        #                 self.ui.label.setEnabled(True)
        #             else:
        #                 self.ui.label.setEnabled(False)
        #         else:
        #             self.pixmap_x64.setVisible(False)
