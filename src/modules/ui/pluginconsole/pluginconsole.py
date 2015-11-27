import os

import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic

import src.conf.settings.SETTINGS as SETTINGS


class PluginConsole(QtGui.QWidget):
    def __init__(self, plugin=None):
        super(PluginConsole, self).__init__()

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'pluginconsole',
                                          'pluginconsole.ui'), self)

        # self.ui.label_plugin_output.setText('{0} {1}'.format(plugin.family, plugin.release_number))
        self.ui.label_plugin_output.setText('')
        self.icon = QtGui.QPixmap(plugin.icon).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT/2.5, QtCore.Qt.SmoothTransformation)
        self.ui.label_plugin_output.setPixmap(self.icon)

        self.show()
