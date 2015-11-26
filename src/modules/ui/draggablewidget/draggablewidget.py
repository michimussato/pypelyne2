import logging
import os
import cPickle

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore

import src.conf.settings.SETTINGS as SETTINGS


class PixmapDraggable(QtGui.QLabel):
    # http://stackoverflow.com/questions/5284648/init-method-for-subclass-of-pyqt-qtablewidgetitem
    def __init__(self, plugin, *args, **kwargs):
        super(PixmapDraggable, self).__init__(*args, **kwargs)

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
        mime_data = QtCore.QMimeData()
        # mime_data.set
        mime_data.setObjectName('node/draggable-pixmap')

        pickled_plugin_object = cPickle.dumps(self.plugin)
        mime_data.setData('node/draggable-pixmap', pickled_plugin_object)
        # mime_data.setText('%d,%d' % (e.x(), e.y()))
        print mime_data.objectName()

        pixmap = QtGui.QPixmap(self.pixmap).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mime_data)
        drag.setPixmap(pixmap)
        drag.setHotSpot(e.pos())

        if drag.exec_(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
            print 'moved'
        else:
            print 'copied'

    def mouseDoubleClickEvent(self, event):
        process = QtCore.QProcess(self)
        # process.setProcessChannelMode(process.MergedChannels)
        process.started.connect(lambda: self.started(plugin=self.plugin))
        process.finished.connect(lambda: self.finished(plugin=self.plugin))
        # process.readyRead.connect(lambda: self.ready_read(process=process))
        process.readyReadStandardOutput.connect(lambda: self.ready_read_stdout(process=process))
        process.readyReadStandardError.connect(lambda: self.ready_read_stderr(process=process))

        process.start(self.plugin.executable, self.plugin.flags)

    def started(self, plugin):
        logging.info('plugin {0} started'.format(plugin.label))

    def finished(self, plugin):
        logging.info('plugin {0} finished'.format(plugin.label))

    def dropEvent(self, event):
        print 'drop'

    def ready_read_stdout(self, process):
        logging.info('process {0} ({1} {2} {3}): {4}'.format(process.pid(),
                                                             self.plugin.family,
                                                             self.plugin.release_number,
                                                             self.plugin.architecture,
                                                             str(process.readAllStandardOutput())))

    def ready_read_stderr(self, process):
        logging.warning('process {0} ({1} {2} {3}): {4}'.format(process.pid(),
                                                                self.plugin.family,
                                                                self.plugin.release_number,
                                                                self.plugin.architecture,
                                                                str(process.readAllStandardError())))
