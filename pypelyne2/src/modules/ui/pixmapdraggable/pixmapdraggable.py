import logging
import cPickle
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.modules.ui.dockwidget.dockwidget_output as dockwidget_output
import pypelyne2.src.modules.ui.compositeicon.compositeicon as compositeicon


class PixmapContainer(QtGui.QLabel):
    def __init__(self, container=None, mainwindow=None, *args, **kwargs):
        super(PixmapContainer, self).__init__(*args, **kwargs)

        self.container = container
        self.mainwindow = mainwindow

        self.pixmap = compositeicon.CompositeIconContainer(self.container).container_icon
        # self.pixmap_hovered

        self.setPixmap(self.pixmap)

    def mouseMoveEvent(self, event):
        logging.info('mouseMoveEvent on {0}'.format(self))
        # http://stackoverflow.com/questions/14395799/pyqt4-drag-and-drop
        mime_data = QtCore.QMimeData()
        mime_data.setObjectName('container/draggable-pixmap')

        pickled_output_object = cPickle.dumps(self.container)
        mime_data.setData('container/draggable-pixmap', pickled_output_object)
        # print mime_data.objectName()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(self.pixmap)
        drag.setHotSpot(event.pos())

        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            pass
        #     print 'moved'
        # else:
        #     print 'copied'

        return QtGui.QLabel.mouseMoveEvent(self, event)

    def enterEvent(self, *args, **kwargs):
        # print 'entered'
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        # self.setPixmap(self.pixmap_hovered)

        # self.emit(QtCore.SIGNAL('PixmapOutput'))

    def leaveEvent(self, *args, **kwargs):
        QtGui.QApplication.restoreOverrideCursor()
        # self.setPixmap(self.pixmap)
        # print 'left'

        # self.emit(QtCore.SIGNAL('PixmapOutput'))


class PixmapOutput(QtGui.QLabel):
    def __init__(self, output=None, mainwindow=None, *args, **kwargs):
        super(PixmapOutput, self).__init__(*args, **kwargs)

        self.output = output
        self.mainwindow = mainwindow

        self.pixmap = compositeicon.CompositeIconOutput(self.output).output_icon
        # self.pixmap_hovered

        self.setPixmap(self.pixmap)

    def mouseMoveEvent(self, event):
        logging.info('mouseMoveEvent on {0}'.format(self))
        # http://stackoverflow.com/questions/14395799/pyqt4-drag-and-drop
        mime_data = QtCore.QMimeData()
        mime_data.setObjectName('output/draggable-pixmap')

        pickled_output_object = cPickle.dumps(self.output)
        mime_data.setData('output/draggable-pixmap', pickled_output_object)
        # print mime_data.objectName()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(self.pixmap)
        drag.setHotSpot(event.pos())

        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            pass
        #     print 'moved'
        # else:
        #     print 'copied'

        return QtGui.QLabel.mouseMoveEvent(self, event)

    def enterEvent(self, *args, **kwargs):
        # print 'entered'
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        # self.setPixmap(self.pixmap_hovered)

        # self.emit(QtCore.SIGNAL('PixmapOutput'))

    def leaveEvent(self, *args, **kwargs):
        QtGui.QApplication.restoreOverrideCursor()
        # self.setPixmap(self.pixmap)
        # print 'left'

        # self.emit(QtCore.SIGNAL('PixmapOutput'))


# pixmap icon base class
class PixmapBase(QtGui.QLabel):
    def __init__(self, plugin=None, mainwindow=None, *args, **kwargs):
        super(PixmapBase, self).__init__(*args, **kwargs)

        self.plugin = plugin
        self.mainwindow = mainwindow

        self.setText('{0} {1}'.format(plugin.family, plugin.release_number))

        self.pixmap = compositeicon.CompositeIcon(self.plugin).pixmap_overlay
        self.pixmap_hovered = compositeicon.CompositeIcon(self.plugin).pixmap_hovered
        self.pixmap_no_overlay = compositeicon.CompositeIcon(self.plugin).pixmap_no_overlay

        self.setPixmap(self.pixmap)

    def enterEvent(self, *args, **kwargs):
        self.setPixmap(self.pixmap_hovered)

        self.emit(QtCore.SIGNAL('PixmapBaseHoverEnter'))

    def leaveEvent(self, *args, **kwargs):
        self.setPixmap(self.pixmap)

        self.emit(QtCore.SIGNAL('PixmapBaseHoverLeave'))

    def started(self, plugin, dock):
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            dock.setWindowTitle(plugin.family)
            self.add_output_dock(dock)
        logging.info('plugin {0} started'.format(plugin.label))

    def finished(self, plugin, dock):
        dock.console.deactivate_buttons()
        if SETTINGS.SHOW_OUTPUT_WINDOWS:
            self.remove_output_dock(dock)
        if SETTINGS.CLOSE_DOCK_AFTER_PLUGIN_CLOSE:
            try:
                self.mainwindow.dock_output_widgets.remove(dock)
            except ValueError, e:
                logging.warning('SHOW_OUTPUT_WINDOWS disabled? {0}'.format(e))
        logging.info('plugin {0} finished'.format(plugin.label))

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


# pixmap drag and drop class, no double click (submitter type)
class PixmapDragAndDrop(PixmapBase):
    def __init__(self, plugin=None, mainwindow=None, *args, **kwargs):
        super(PixmapDragAndDrop, self).__init__(plugin, mainwindow, *args, **kwargs)

        self.drag_cursor = QtGui.QCursor(QtCore.Qt.OpenHandCursor)

        self.connect(self, QtCore.SIGNAL('PixmapBaseHoverEnter'), self.hover_enter)
        self.connect(self, QtCore.SIGNAL('PixmapBaseHoverLeave'), self.hover_leave)

    def hover_enter(self):
        logging.info('hover_enter on PixmapDragAndDrop ({0})'.format(self))
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

    def hover_leave(self):
        logging.info('hover_leave on PixmapDragAndDrop ({0})'.format(self))
        QtGui.QApplication.restoreOverrideCursor()

    def mouseMoveEvent(self, event):
        logging.info('mouseMoveEvent on {0}'.format(self))
        # http://stackoverflow.com/questions/14395799/pyqt4-drag-and-drop
        mime_data = QtCore.QMimeData()
        mime_data.setObjectName('node/draggable-pixmap')

        pickled_plugin_object = cPickle.dumps(self.plugin)
        mime_data.setData('node/draggable-pixmap', pickled_plugin_object)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(self.pixmap_no_overlay)
        drag.setHotSpot(event.pos())

        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            pass
        #     print 'moved'
        # else:
        #     print 'copied'

        return QtGui.QLabel.mouseMoveEvent(self, event)

    # def enterEvent(self, *args, **kwargs):
    #     QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
    #
    # def leaveEvent(self, *args, **kwargs):
    #     QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def dropEvent(self, event):
        logging.info('dropEvent on {0}'.format(self))


# pixmap double click, no drag and drop (plugin type)
class PixmapNodeableFalse(PixmapBase):
    def __init__(self, plugin=None, mainwindow=None, *args, **kwargs):
        super(PixmapNodeableFalse, self).__init__(plugin, mainwindow, *args, **kwargs)

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


# pixmap with drag and drop and double click (standalone type)
class PixmapFullFeature(PixmapDragAndDrop, PixmapNodeableFalse):
    def __init__(self, plugin=None, mainwindow=None, *args, **kwargs):
        super(PixmapFullFeature, self).__init__(plugin, mainwindow, *args, **kwargs)
