import sys

import PyQt4.QtGui as QtGui

import src.modules.ui.mainwindow.mainwindow as mainwindow

app = QtGui.QApplication(sys.argv)
# screen_size = QtGui.QApplication.desktop().availableGeometry()
scene = mainwindow.MainWindow()
# scene.resize(int(screen_size.width()), int(screen_size.height()))
scene.show()
app.exec_()
