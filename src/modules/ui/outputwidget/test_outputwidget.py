import sys

import PyQt4.QtGui as QtGui

import src.modules.ui.outputwidget.outputwidget as outputwidget
import src.parser.parse_outputs as parse_outputs


plugins = parse_outputs.get_outputs()
print dir(plugins[0])

app = QtGui.QApplication(sys.argv)

scene = outputwidget.OutputWidget(plugins[1])

scene.show()
app.exec_()
