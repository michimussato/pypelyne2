import os
import logging
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import PyQt4.uic as uic
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class PortHover(QtGui.QWidget):
    def __init__(self, output_object=None):
        super(PortHover, self).__init__()

        self.output = output_object

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'porthover',
                                          'porthover.ui'), self)

        self.palette = QtGui.QPalette()

    def set_palette(self):
        self.palette.setColor(QtGui.QWidget().backgroundRole(), QtGui.QColor(50, 50, 50, 0))
        if SETTINGS.TRANSPARENT_OUTPUT_LABEL:
            self.ui.setPalette(self.palette)

    def wheelEvent(self, event):
        logging.info('wheelEvent on PortHover ({0})'.format(self))
        event.ignore()


class OutputHover(PortHover):
    def __init__(self, output_object=None):
        super(OutputHover, self).__init__()

        self.output = output_object

        self.setup_title()

    def setup_title(self):
        self.ui.label_title.setToolTip('shift+left click to change name')
        self.ui.label_title_edit.setToolTip('enter to submit')
        self.ui.label_title_edit.setText(self.ui.label_title.text())

        self.ui.label_title_edit.setVisible(False)
        self.ui.label_title.setVisible(True)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on OutputHover ({0})'.format(self))
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()

        if keyboard_modifiers == QtCore.Qt.ShiftModifier and event.button() == QtCore.Qt.LeftButton:
            self.ui.label_title.setVisible(False)
            self.ui.label_title_edit.setVisible(True)
            self.ui.label_title_edit.setReadOnly(False)
            self.ui.label_title_edit.setFocus()
            self.ui.label_title_edit.selectAll()
            return

        return OutputHover.mouseMoveEvent(self, event)


class InputHover(OutputHover):
    def __init__(self, output_object=None):
        super(OutputHover, self).__init__()

        self.output = output_object

        self.set_palette()

        self.setup_title()

    def setup_title(self):
        self.ui.label_title.setToolTip('change name at source')
        # self.ui.label_title_edit.setToolTip('enter to submit')
        self.ui.label_title_edit.setText(self.ui.label_title.text())

        self.ui.label_title_edit.setVisible(False)
        self.ui.label_title.setVisible(True)

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on OutputHover ({0})'.format(self))
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()

        if keyboard_modifiers == QtCore.Qt.ShiftModifier and event.button() == QtCore.Qt.LeftButton:
            return

        return OutputHover.mouseMoveEvent(self, event)
