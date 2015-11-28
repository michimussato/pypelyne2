import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import src.conf.settings.SETTINGS as SETTINGS
import src.modules.ui.compositeicon.compositeicon as compositeicon


class PluginConsole(QtGui.QWidget):
    def __init__(self, plugin=None):
        super(PluginConsole, self).__init__()

        self.plugin = plugin

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'pluginconsole',
                                          'pluginconsole.ui'), self)

        self.ui.label_plugin_icon.setText('')
        self.ui.label_plugin_version.setText(self.plugin.release_number)
        self.icon = compositeicon.CompositeIcon(self.plugin).pixmap_no_arch.scaledToHeight(SETTINGS.ICON_HEIGHT,
                                                                                           QtCore.Qt.SmoothTransformation)
        self.arch_icon = compositeicon.CompositeIcon(self.plugin).arch_icon.scaledToHeight(SETTINGS.ICON_HEIGHT,
                                                                                           QtCore.Qt.SmoothTransformation)
        self.ui.label_plugin_icon.setPixmap(self.icon)
        self.ui.label_arch_icon.setPixmap(self.arch_icon)

        self.show()
