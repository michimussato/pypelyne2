import os
from PyQt4 import QtGui
from PyQt4 import QtCore
import PyQt4.uic as uic

import src.modules.ui.dockwidget.dockwidget as dockwidget
import src.modules.ui.pluginwidget.pluginwidget as pluginwidget
# import src.modules.ui.graphicsview.graphicsview as graphicsview

import src.parser.parse_plugins as parse_plugins

import src.conf.settings.SETTINGS as SETTINGS


class DockWidgetPlugins(dockwidget.DockWidget):
    def __init__(self):
        super(DockWidgetPlugins, self).__init__()

        self.setWindowTitle('DockWidgetPlugins')

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        self.setFeatures(QtGui.QDockWidget.DockWidgetFloatable | QtGui.QDockWidget.DockWidgetMovable)

        self.plugins = parse_plugins.get_plugins()

        widget = QtGui.QWidget()
        self.layout_plugins = QtGui.QVBoxLayout()

        for plugin in self.plugins:
            if plugin.family_enable:
                if SETTINGS.DISPLAY_ONLY_AVAILABLE and plugin.executable_x32 is None and plugin.executable_x64 is None:
                    pass
                else:
                    # print dir(plugin)
                    plugin_widget = pluginwidget.PluginWidget(plugin)
                    self.layout_plugins.addWidget(plugin_widget)

        widget.setLayout(self.layout_plugins)

        scroll = QtGui.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(False)
        scroll.setWidget(widget)

        container_layout = QtGui.QVBoxLayout()
        container_layout.addWidget(scroll)
        container_widget = QtGui.QWidget()
        container_widget.setLayout(container_layout)
        self.setWidget(container_widget)
