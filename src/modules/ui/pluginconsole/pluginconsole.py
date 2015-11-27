import os

import PyQt4.QtGui as QtGui
import PyQt4.uic as uic

import src.conf.settings.SETTINGS as SETTINGS


class PluginConsole(QtGui.QWidget):
    def __init__(self):
        super(PluginConsole, self).__init__()

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'pluginconsole',
                                          'pluginconsole.ui'), self)
        self.show()