import logging
import datetime

from PyQt4 import QtGui
from PyQt4 import QtCore

import src.modules.ui.dockwidget.dockwidget as dockwidget
import src.modules.ui.pluginconsole.pluginconsole as pluginconsole

import src.conf.settings.SETTINGS as SETTINGS


class DockWidgetOutput(dockwidget.DockWidget):
    def __init__(self, mainwindow=None):
        super(DockWidgetOutput, self).__init__()

        self.mainwindow = mainwindow

        self.setWindowTitle('DockWidgetOutput')

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self.console = pluginconsole.PluginConsole()

        self.setWidget(self.console)

    def data_ready_std(self, process):
    # def data_ready_std(self, process, process_color):
        box = self.console.ui.output_area_std
        cursor_box = box.textCursor()
        cursor_box.movePosition(cursor_box.End)

        # std_format = cursor_box.charFormat()
        # new_format = cursor_box.charFormat()

        # std_format.setBackground(QtCore.Qt.white)
        # std_format.setForeground(QtCore.Qt.black)

        # modify it
        # new_format.setBackground(process_color)
        # new_format.setForeground(process_color.lighter(160))
        # apply it
        # cursor_box.setCharFormat(new_format)

        cursor_box.insertText('%s (std):   %s' % (datetime.datetime.now(), str(process.readAllStandardOutput())))
        # logging.info('%s (std):   %s' % (datetime.datetime.now(), str(process.readAllStandardOutput())))

        cursor_box.movePosition(cursor_box.End)
        # char_format = cursor_box.charFormat()
        # char_format.setBackground(QtCore.Qt.white)
        # char_format.setForeground(QtCore.Qt.black)
        # cursor_box.setCharFormat(std_format)

        cursor_box.insertText('\n')

        box.ensureCursorVisible()

    def data_ready_err(self, process):
    # def data_ready_std(self, process, process_color):
        box = self.console.ui.output_area_err
        cursor_box = box.textCursor()
        cursor_box.movePosition(cursor_box.End)

        # std_format = cursor_box.charFormat()
        # new_format = cursor_box.charFormat()

        # std_format.setBackground(QtCore.Qt.white)
        # std_format.setForeground(QtCore.Qt.black)

        # modify it
        # new_format.setBackground(process_color)
        # new_format.setForeground(process_color.lighter(160))
        # apply it
        # cursor_box.setCharFormat(new_format)

        cursor_box.insertText('%s (err):   %s' % (datetime.datetime.now(), str(process.readAllStandardOutput())))
        # logging.info('%s (err):   %s' % (datetime.datetime.now(), str(process.readAllStandardOutput())))

        cursor_box.movePosition(cursor_box.End)
        # char_format = cursor_box.charFormat()
        # char_format.setBackground(QtCore.Qt.white)
        # char_format.setForeground(QtCore.Qt.black)
        # cursor_box.setCharFormat(std_format)

        cursor_box.insertText('\n')

        box.ensureCursorVisible()