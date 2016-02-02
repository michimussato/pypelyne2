import logging
import sys
import os
import PyQt4.QtGui as QtGui
import pypelyne2.src.modules.ui.mainwindow.mainwindow as mainwindow
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


logging.info('Python version: {0}'.format(SETTINGS.VERSION_PYTHON))
logging.info('Qt version:     {0}'.format(SETTINGS.VERSION_QT))
logging.info('SIP version:    {0}'.format(SETTINGS.VERSION_SIP))
logging.info('PyQt version:   {0}'.format(SETTINGS.VERSION_PYQT))


app = QtGui.QApplication(sys.argv)
if SETTINGS.QSS_ENABLE:
    with open(os.path.join(SETTINGS.QSS_FILE), 'r') as qss:
        style = qss.read()
        app.setStyleSheet(style)
app.setWindowIcon(QtGui.QIcon(SETTINGS.SPLASH_ICON))
screen_size = QtGui.QApplication.desktop().availableGeometry()
scene = mainwindow.MainWindow()
scene.resize(int(screen_size.width()), int(screen_size.height()))
scene.show()
scene.raise_()
app.exec_()
