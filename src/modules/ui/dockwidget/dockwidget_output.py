import datetime
import PyQt4.QtCore as QtCore
import src.modules.ui.dockwidget.dockwidget as dockwidget
import src.modules.ui.pluginconsole.pluginconsole as pluginconsole


class DockWidgetOutput(dockwidget.DockWidget):
    def __init__(self, pixmapdraggable=None, plugin=None):
        super(DockWidgetOutput, self).__init__()

        self.pixmapdraggable = pixmapdraggable
        self.plugin = plugin

        self.setWindowTitle('DockWidgetOutput')

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self.console = pluginconsole.PluginConsole(self.plugin)

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
        self.pixmapdraggable.mainwindow.dock_output_widgets.remove(self)
