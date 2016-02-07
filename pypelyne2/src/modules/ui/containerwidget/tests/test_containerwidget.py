import sys
import PyQt4.QtGui as QtGui
import pypelyne2.src.modules.ui.containerwidget.containerwidget as containerwidget
import pypelyne2.src.parser.parse_containers as parse_containers


containers = parse_containers.get_containers()
print dir(containers[0])

for attr in dir(containers[0]):
    print getattr(containers[0], attr)

app = QtGui.QApplication(sys.argv)

scene = containerwidget.ContainerWidget(containers[0])

scene.show()
scene.raise_()
app.exec_()
