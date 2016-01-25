import datetime
import PyQt4.QtCore as QtCore
import pypelyne2.src.modules.ui.dockwidget.dockwidget as dockwidget
import pypelyne2.src.modules.ui.pluginconsole.pluginconsole as pluginconsole


class DockWidgetOutput(dockwidget.DockWidget):
    def __init__(self, pixmapdraggable=None, plugin=None, process=None):
        super(DockWidgetOutput, self).__init__()

        self.pixmapdraggable = pixmapdraggable
        self.plugin = plugin
        self.process = process

        self.setWindowTitle('DockWidgetOutput')

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self.console = pluginconsole.PluginConsole(self.plugin, self.process)

        self.setWidget(self.console)

    def data_ready_std(self):
        box = self.console.ui.output_area_std
        cursor_box = box.textCursor()
        cursor_box.movePosition(cursor_box.End)
        cursor_box.insertText('{0} (std):   {1}'.format(datetime.datetime.now(), str(self.process.readAllStandardOutput())))
        cursor_box.movePosition(cursor_box.End)
        cursor_box.insertText('\n')
        box.ensureCursorVisible()

    def data_ready_err(self):
        box = self.console.ui.output_area_err
        cursor_box = box.textCursor()
        cursor_box.movePosition(cursor_box.End)
        cursor_box.insertText('{0} (err):   {1}'.format(datetime.datetime.now(), str(self.process.readAllStandardOutput())))
        cursor_box.movePosition(cursor_box.End)
        cursor_box.insertText('\n')
        box.ensureCursorVisible()

    def closeEvent(self, event):
        self.pixmapdraggable.mainwindow.dock_output_widgets.remove(self)
