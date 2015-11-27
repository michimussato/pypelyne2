import logging
import os
import cPickle

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import src.conf.settings.SETTINGS as SETTINGS
import src.modules.ui.dockwidget.dockwidget_output as dockwidget_output


class PixmapDraggable(QtGui.QLabel):
    # http://stackoverflow.com/questions/5284648/init-method-for-subclass-of-pyqt-qtablewidgetitem
    def __init__(self, plugin=None, mainwindow=None, *args, **kwargs):
        super(PixmapDraggable, self).__init__(*args, **kwargs)

        self.plugin = plugin
        self.mainwindow = mainwindow

        self.setText('{} {}'.format(plugin.family, plugin.release_number))

        if plugin.icon is None:
            icon = QtGui.QPixmap(SETTINGS.PLUGINS_DEFAULT_ICON)
        else:
            icon = QtGui.QPixmap(os.path.join(SETTINGS.PLUGINS_ICONS, plugin.icon))
        self.icon = icon.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT, QtCore.Qt.SmoothTransformation)

        self.pixmap = QtGui.QPixmap(SETTINGS.PLUGINS_ICON_HEIGHT, SETTINGS.PLUGINS_ICON_HEIGHT)
        self.pixmap_hovered = QtGui.QPixmap(SETTINGS.PLUGINS_ICON_HEIGHT, SETTINGS.PLUGINS_ICON_HEIGHT)

        if plugin.architecture == 'x32':
            arch_icon = QtGui.QPixmap(SETTINGS.ICON_X32)
        elif plugin.architecture == 'x64':
            arch_icon = QtGui.QPixmap(SETTINGS.ICON_X64)
        self.arch_icon = arch_icon.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT/2.5, QtCore.Qt.SmoothTransformation)

        self.create_pixmap()
        self.create_pixmap_hovered()
        self.setPixmap(self.pixmap)

    def create_pixmap(self):
        color = QtGui.QColor(0, 0, 0, 0)
        self.pixmap.fill(color)

        painter = QtGui.QPainter()
        painter.begin(self.pixmap)
        # http://doc.qt.io/qt-4.8/qpainter.html#CompositionMode-enum
        painter.setCompositionMode(painter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, self.icon)
        painter.drawPixmap(0, 0, self.arch_icon)
        painter.end()

    def create_pixmap_hovered(self):
        color_hovered = QtGui.QColor(255, 255, 255, 255)
        self.pixmap_hovered.fill(color_hovered)

        painter_hovered = QtGui.QPainter()
        painter_hovered.begin(self.pixmap_hovered)
        painter_hovered.setCompositionMode(painter_hovered.CompositionMode_SourceOver)
        painter_hovered.drawPixmap(0, 0, self.pixmap_hovered)
        painter_hovered.drawPixmap(0, 0, self.pixmap)
        painter_hovered.end()

    def mouseMoveEvent(self, e):
        # http://stackoverflow.com/questions/14395799/pyqt4-drag-and-drop
        mime_data = QtCore.QMimeData()
        mime_data.setObjectName('node/draggable-pixmap')

        pickled_plugin_object = cPickle.dumps(self.plugin)
        mime_data.setData('node/draggable-pixmap', pickled_plugin_object)
        print mime_data.objectName()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(self.pixmap)
        drag.setHotSpot(e.pos())

        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            print 'moved'
        else:
            print 'copied'

    def enterEvent(self, *args, **kwargs):
        # print 'entered'
        self.setPixmap(self.pixmap_hovered)

    def leaveEvent(self, *args, **kwargs):
        self.setPixmap(self.pixmap)
        # print 'left'

    def mouseDoubleClickEvent(self, event):
        output_dock = None
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            output_dock = dockwidget_output.DockWidgetOutput(self)
        process = QtCore.QProcess(self)
        process.started.connect(lambda: self.started(plugin=self.plugin, dock=output_dock))
        process.finished.connect(lambda: self.finished(plugin=self.plugin, dock=output_dock))
        process.readyReadStandardOutput.connect(lambda: self.ready_read_stdout(process=process, dock=output_dock))
        process.readyReadStandardError.connect(lambda: self.ready_read_stderr(process=process, dock=output_dock))

        process.start(self.plugin.executable, self.plugin.flags)

    def started(self, plugin, dock):
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            dock.setWindowTitle(plugin.label)
            self.add_output_dock(plugin, dock)
        logging.info('plugin {0} started'.format(plugin.label))

    def finished(self, plugin, dock):
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            self.remove_output_dock(plugin, dock)
        logging.info('plugin {0} finished'.format(plugin.label))

    def dropEvent(self, event):
        print 'drop'

    def ready_read_stdout(self, process, dock):
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            dock.data_ready_std(process)
        logging.info('process {0} ({1} {2} {3}): {4}'.format(process.pid(),
                                                             self.plugin.family,
                                                             self.plugin.release_number,
                                                             self.plugin.architecture,
                                                             str(process.readAllStandardOutput())))

    def ready_read_stderr(self, process, dock):
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            dock.data_ready_err(process)
        logging.warning('process {0} ({1} {2} {3}): {4}'.format(process.pid(),
                                                                self.plugin.family,
                                                                self.plugin.release_number,
                                                                self.plugin.architecture,
                                                                str(process.readAllStandardError())))

    def add_output_dock(self, plugin, dock):
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            self.mainwindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
            if SETTINGS.TABIFY_OUTPUT_WINDOWS:
                if bool(self.mainwindow.dock_output_widgets):
                    self.mainwindow.tabifyDockWidget(self.mainwindow.dock_output_widgets[0], dock)
            self.mainwindow.dock_output_widgets.append(dock)

    def remove_output_dock(self, plugin, dock):
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            dock.setFeatures(dock.DockWidgetFloatable | dock.DockWidgetMovable | dock.DockWidgetClosable)
            if SETTINGS.CLOSE_DOCK_AFTER_PLUGIN_CLOSE:
                self.mainwindow.removeDockWidget(dock)
