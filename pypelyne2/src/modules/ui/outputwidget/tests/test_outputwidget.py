import sys
import PyQt4.QtGui as QtGui
import pypelyne2.src.modules.ui.outputwidget.outputwidget as outputwidget
import pypelyne2.src.parser.parse_outputs as parse_outputs


outputs = parse_outputs.get_outputs()
print dir(outputs[0])

for attr in dir(outputs[0]):
    print getattr(outputs[0], attr)

app = QtGui.QApplication(sys.argv)

scene = outputwidget.OutputWidget(outputs[0])

scene.show()
scene.raise_()
app.exec_()
