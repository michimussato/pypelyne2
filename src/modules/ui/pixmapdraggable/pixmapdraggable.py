import logging
import cPickle
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import src.conf.settings.SETTINGS as SETTINGS
import src.modules.ui.dockwidget.dockwidget_output as dockwidget_output
import src.modules.ui.compositeicon.compositeicon as compositeicon


class PixmapDraggable(QtGui.QLabel):
    # http://stackoverflow.com/questions/5284648/init-method-for-subclass-of-pyqt-qtablewidgetitem
    def __init__(self, plugin=None, mainwindow=None, *args, **kwargs):
        super(PixmapDraggable, self).__init__(*args, **kwargs)

        self.plugin = plugin
        self.mainwindow = mainwindow

        self.setText('{0} {1}'.format(plugin.family, plugin.release_number))

        self.pixmap = compositeicon.CompositeIcon(self.plugin).pixmap
        self.pixmap_hovered = compositeicon.CompositeIcon(self.plugin).pixmap_hovered
        self.pixmap_noarch = compositeicon.CompositeIcon(self.plugin).pixmap_no_arch

        self.setPixmap(self.pixmap)

    def mouseMoveEvent(self, e):
        # http://stackoverflow.com/questions/14395799/pyqt4-drag-and-drop
        mime_data = QtCore.QMimeData()
        mime_data.setObjectName('node/draggable-pixmap')

        pickled_plugin_object = cPickle.dumps(self.plugin)
        mime_data.setData('node/draggable-pixmap', pickled_plugin_object)
        print mime_data.objectName()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(self.pixmap_noarch)
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
        # if SETTINGS.SHOW_OUTPUT_WINDOWS:
        #     output_dock = dockwidget_output.DockWidgetOutput(self, self.plugin)
        process = QtCore.QProcess(self)
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            output_dock = dockwidget_output.DockWidgetOutput(self, self.plugin, process)
        process.started.connect(lambda: self.started(plugin=self.plugin, dock=output_dock))
        process.finished.connect(lambda: self.finished(plugin=self.plugin, dock=output_dock))
        process.readyReadStandardOutput.connect(lambda: self.ready_read_stdout(process=process, dock=output_dock))
        process.readyReadStandardError.connect(lambda: self.ready_read_stderr(process=process, dock=output_dock))

        process.start(self.plugin.executable, self.plugin.flags)

    def started(self, plugin, dock):
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            dock.setWindowTitle(plugin.family)
            self.add_output_dock(dock)
        logging.info('plugin {0} started'.format(plugin.label))

    def finished(self, plugin, dock):
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            self.remove_output_dock(dock)
        if SETTINGS.CLOSE_DOCK_AFTER_PLUGIN_CLOSE:
            try:
                self.mainwindow.dock_output_widgets.remove(dock)
            except ValueError, e:
                logging.warning('SHOW_OUTPUT_WINDOWS disabled? {0}'.format(e))
        logging.info('plugin {0} finished'.format(plugin.label))

    def dropEvent(self, event):
        print 'drop'

    def ready_read_stdout(self, process, dock):
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            dock.data_ready_std()
        logging.info('process {0} ({1} {2} {3}): {4}'.format(process.pid(),
                                                             self.plugin.family,
                                                             self.plugin.release_number,
                                                             self.plugin.architecture,
                                                             str(process.readAllStandardOutput())))

    def ready_read_stderr(self, process, dock):
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            dock.data_ready_err()
        logging.warning('process {0} ({1} {2} {3}): {4}'.format(process.pid(),
                                                                self.plugin.family,
                                                                self.plugin.release_number,
                                                                self.plugin.architecture,
                                                                str(process.readAllStandardError())))

    def add_output_dock(self, dock):
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            self.mainwindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
            if SETTINGS.TABIFY_OUTPUT_WINDOWS:
                if bool(self.mainwindow.dock_output_widgets):
                    self.mainwindow.tabifyDockWidget(self.mainwindow.dock_output_widgets[0], dock)
            self.mainwindow.dock_output_widgets.append(dock)

    def remove_output_dock(self, dock):
        dock.setFeatures(dock.DockWidgetFloatable | dock.DockWidgetMovable | dock.DockWidgetClosable)
        if SETTINGS.CLOSE_DOCK_AFTER_PLUGIN_CLOSE:
            self.mainwindow.removeDockWidget(dock)
