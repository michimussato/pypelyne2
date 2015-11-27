import datetime

from PyQt4 import QtCore

import src.modules.ui.dockwidget.dockwidget as dockwidget
import src.modules.ui.pluginconsole.pluginconsole as pluginconsole


class DockWidgetOutput(dockwidget.DockWidget):
    def __init__(self, pixmapdraggable=None):
        super(DockWidgetOutput, self).__init__()

        # self.mainwindow = mainwindow
        self.pixmapdraggable = pixmapdraggable

        self.setWindowTitle('DockWidgetOutput')

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self.console = pluginconsole.PluginConsole()

        self.setWidget(self.console)

    def data_ready_std(self, process):
        box = self.console.ui.output_area_std
        cursor_box = box.textCursor()
        cursor_box.movePosition(cursor_box.End)
        cursor_box.insertText('{0} (std):   {1}'.format(datetime.datetime.now(), str(process.readAllStandardOutput())))
        cursor_box.movePosition(cursor_box.End)
        cursor_box.insertText('\n')
        box.ensureCursorVisible()

    def data_ready_err(self, process):
        box = self.console.ui.output_area_err
        cursor_box = box.textCursor()
        cursor_box.movePosition(cursor_box.End)
        cursor_box.insertText('{0} (err):   {1}'.format(datetime.datetime.now(), str(process.readAllStandardOutput())))
        cursor_box.movePosition(cursor_box.End)
        cursor_box.insertText('\n')
        box.ensureCursorVisible()

    def closeEvent(self, event):
        # print self.pixmapdraggable.mainwindow.dock_output_widgets
        self.pixmapdraggable.mainwindow.dock_output_widgets.remove(self)
        # print self.pixmapdraggable.mainwindow.dock_output_widgets
