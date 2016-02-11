import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.modules.ui.dockwidget.dockwidget as dockwidget
import pypelyne2.src.modules.ui.pluginwidget.pluginwidget as pluginwidget
import pypelyne2.src.parser.parse_plugins as parse_plugins
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class DockWidgetPlugins(dockwidget.DockWidget):
    def __init__(self, mainwindow=None):
        super(DockWidgetPlugins, self).__init__()

        self.mainwindow = mainwindow

        self.setWindowTitle('Plugins')

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self.plugins = parse_plugins.get_plugins()

        widget = QtGui.QWidget()
        self.layout_plugins = QtGui.QVBoxLayout()

        for plugin in self.plugins:
            if plugin.family_enable:
                # print plugin.family
                # print dir(plugin)
                if hasattr(plugin, 'executable'):
                    # this is needed for arch agnostic plugins
                    if SETTINGS.DISPLAY_ONLY_AVAILABLE and plugin.executable is None:
                        pass
                    else:
                        plugin_widget = pluginwidget.PluginWidget(plugin=plugin, mainwindow=mainwindow)
                        self.layout_plugins.addWidget(plugin_widget)

                elif hasattr(plugin, 'executable_x32') and hasattr(plugin, 'executable_x64'):
                    # this is needed for arch aware plugins
                    if SETTINGS.DISPLAY_ONLY_AVAILABLE and plugin.executable_x32 is None and plugin.executable_x64 is None:
                        pass
                    else:
                        plugin_widget = pluginwidget.PluginWidget(plugin=plugin, mainwindow=mainwindow)
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
