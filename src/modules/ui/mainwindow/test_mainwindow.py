import sys

import PyQt4.QtGui as QtGui

import src.modules.ui.mainwindow.mainwindow as mainwindow

app = QtGui.QApplication(sys.argv)
# screen_size = QtGui.QApplication.desktop().availableGeometry()
scene = mainwindow.MainWindow()
# scene.resize(int(screen_size.width()), int(screen_size.height()))
scene.show()
app.exec_()

# app = QtGui.QApplication(sys.argv)
#
# splash = QtGui.QPixmap(ICON_DEFAULT)
# splash = QtGui.QSplashScreen(splash, QtCore.Qt.WindowStaysOnTopHint)
# splash.setMask(splash.mask())
# splash.show()
# app.processEvents()
#
# from applauncher_ui import AppLauncherUI
# app_launcher = AppLauncherUI(studio='')
# splash.finish(app_launcher)
# return app.exec_()
