import sys

import PyQt4.QtGui as QtGui

import src.modules.ui.pluginwidget.pluginwidget as pluginwidget
import src.parser.parse_plugins as parse_plugins


plugins = parse_plugins.get_plugins()
print dir(plugins[0])

app = QtGui.QApplication(sys.argv)

scene = pluginwidget.PluginWidget(plugins[1])

scene.show()
app.exec_()
