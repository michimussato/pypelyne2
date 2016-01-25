import logging
import sys
import os
import PyQt4.QtGui as QtGui
# from PyQt4.QtCore import QT_VERSION_STR
from PyQt4.QtCore import QT_VERSION_STR
from PyQt4.Qt import PYQT_VERSION_STR
from sip import SIP_VERSION_STR
# from PyQt4.Qt import PYQT_VERSION_STR
# from sip import SIP_VERSION_STR
import pypelyne2.src.modules.ui.mainwindow.mainwindow as mainwindow
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


logging.info('Qt version:'.format(QT_VERSION_STR))
logging.info('SIP version:'.format(SIP_VERSION_STR))
logging.info('PyQt version:'.format(PYQT_VERSION_STR))


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
