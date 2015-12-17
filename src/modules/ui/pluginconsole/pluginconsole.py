import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import src.conf.settings.SETTINGS as SETTINGS
import src.modules.ui.compositeicon.compositeicon as compositeicon
import src.modules.screengrabber2.screengrabber2 as screengrabber


class PluginConsole(QtGui.QWidget):
    def __init__(self, plugin=None, process=None):
        super(PluginConsole, self).__init__()

        self.plugin = plugin
        self.process = process
        self.grabber = screengrabber.ScreenGrabber()

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'pluginconsole',
                                          'pluginconsole.ui'), self)

        if SETTINGS.HIDE_CONSOLE:
            self.ui.splitter.setVisible(False)

        self.icon = compositeicon.CompositeIcon(self.plugin).pixmap_no_overlay.scaledToHeight(SETTINGS.ICON_HEIGHT,
                                                                                              QtCore.Qt.SmoothTransformation)
        self.arch_icon = compositeicon.CompositeIcon(self.plugin).overlay_icon.scaledToHeight(SETTINGS.ICON_HEIGHT,
                                                                                              QtCore.Qt.SmoothTransformation)

        self.apply_grabber_settings()

        self.set_button_look()
        self.create_connects()

        self.show()

    def apply_grabber_settings(self):
        if SETTINGS.GRABBER_AUTO_START:
            self.set_play()
            self.grabber_start()
        else:
            self.set_stop()

    def set_play(self):
        self.ui.push_button_capture_start.setVisible(False)
        self.ui.push_button_capture_stop.setVisible(True)

    def set_stop(self):
        self.ui.push_button_capture_stop.setVisible(False)
        self.ui.push_button_capture_start.setVisible(True)

    def set_button_look(self):
        self.ui.label_plugin_icon.setText('')
        self.ui.label_plugin_version.setText(self.plugin.release_number)
        self.ui.push_button_capture_start.setText('')
        self.ui.push_button_capture_stop.setText('')
        self.ui.push_button_kill.setText('')

        self.ui.push_button_capture_start.setFlat(True)
        self.ui.push_button_capture_stop.setFlat(True)
        self.ui.push_button_kill.setFlat(True)

        self.set_icons()

    def set_icons(self):
        self.ui.label_plugin_icon.setPixmap(self.icon)
        self.ui.label_arch_icon.setPixmap(self.arch_icon)
        self.ui.push_button_capture_start.setIcon(QtGui.QIcon(SETTINGS.CAPTURE_ICON_START))
        self.ui.push_button_capture_stop.setIcon(QtGui.QIcon(SETTINGS.CAPTURE_ICON_STOP))
        self.ui.push_button_kill.setIcon(QtGui.QIcon(SETTINGS.KILL_ICON))

    def create_connects(self):
        self.ui.push_button_capture_start.clicked.connect(self.grabber_start)
        self.ui.push_button_capture_stop.clicked.connect(self.grabber_stop)
        self.ui.push_button_kill.clicked.connect(self.kill)

    def grabber_start(self):
        # self.grabber.start_capture()
        self.set_play()
        self.ui.push_button_capture_start.setVisible(False)
        self.ui.push_button_capture_stop.setVisible(True)

    def grabber_stop(self):
        # self.grabber.stop_capture()
        self.set_stop()

    # def app_close(self):
    #     self.grabber_stop()
    #     # self.grabber.stop_capture()

    # def terminate(self):
    #     self.grabber_stop()
    #     # self.grabber.stop_capture()
    #     self.ui.push_button_capture_start.setEnabled(False)
    #     self.ui.push_button_capture_stop.setEnabled(False)
    #     self.process.terminate()

    def deactivate_buttons(self):
        self.grabber_stop()
        self.ui.push_button_kill.setEnabled(False)
        self.ui.push_button_capture_start.setEnabled(False)
        self.ui.push_button_capture_stop.setEnabled(False)

    def kill(self):
        # self.grabber_stop()
        self.deactivate_buttons()
        # self.process.terminate()
        self.process.kill()
