import sys

import PyQt4.QtGui as QtGui

import src.modules.ui.outputwidget.outputwidget as outputwidget
import src.parser.parse_outputs as parse_outputs


outputs = parse_outputs.get_outputs()
print dir(outputs[0])

app = QtGui.QApplication(sys.argv)

scene = outputwidget.OutputWidget(outputs[1])

scene.show()
scene.raise_()
app.exec_()
