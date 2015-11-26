import sys

import PyQt4.QtGui as QtGui

import src.modules.ui.mainwindow.mainwindow as mainwindow
import src.conf.settings.SETTINGS as SETTINGS

app = QtGui.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(SETTINGS.SPLASH_ICON))
# screen_size = QtGui.QApplication.desktop().availableGeometry()
scene = mainwindow.MainWindow()
# scene.resize(int(screen_size.width()), int(screen_size.height()))
scene.show()
scene.raise_()
app.exec_()
