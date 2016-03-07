import sys

import PyQt4.QtGui as QtGui

import pypelyne2.src.modules.core.parser.parse_plugins as parse_plugins
import pypelyne2.src.modules.ui.pluginwidget.pluginwidget as pluginwidget

plugins = parse_plugins.get_plugins()
print dir(plugins[0])

app = QtGui.QApplication(sys.argv)

scene = pluginwidget.PluginWidget(plugins[1])

scene.show()
scene.raise_()
app.exec_()
