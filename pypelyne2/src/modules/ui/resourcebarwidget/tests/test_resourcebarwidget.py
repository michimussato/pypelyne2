import sys
import PyQt4.QtGui as QtGui
import pypelyne2.src.modules.ui.resourcebarwidget.resourcebarwidget as resourcebarwidget

app = QtGui.QApplication(sys.argv)
# screen_size = QtGui.QApplication.desktop().availableGeometry()
scene = resourcebarwidget.ResourceBarWidget()

# scene.resize(int(screen_size.width()), int(screen_size.height()))
scene.show()
scene.raise_()
app.exec_()
