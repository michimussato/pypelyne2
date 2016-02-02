import os
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import pypelyne2.src.modules.ui.compositeicon.compositeicon as compositeicon


class Container(QtGui.QWidget):
    def __init__(self):
        super(Container, self).__init__()

        # self.plugin = plugin
        # self.process = process
        # self.grabber = screengrabber.ScreenGrabber()

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          '_research',
                                          'container.ui'), self)
