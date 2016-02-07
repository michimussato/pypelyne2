import logging
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class LabelGif(QtGui.QLabel):
    def __init__(self, node_object=None):
        super(LabelGif, self).__init__()

        self.dialog = QtGui.QFileDialog()

        self.node = node_object

    def mousePressEvent(self, event):
        logging.info('mousePressEvent on QLabelGif ({0})'.format(self))
        keyboard_modifiers = QtGui.QApplication.keyboardModifiers()
        if event.button() == QtCore.Qt.RightButton:
            if keyboard_modifiers == QtCore.Qt.ShiftModifier:
                # self.dialog.setFileMode(self.dialog.fileMode())
                # self.dialog.setFilter(QtCore.QDir.Files | QtCore.QDir.NoDotAndDotDot)
                dialog = self.dialog.getOpenFileName(self, 'get preview icon', SETTINGS.PYPELYNE2_ROOT)
                # TODO: cancel still picks a new random image
                print dialog
                # print ok
                self.node.update_thumbnail_icon(dialog)
            else:
                self.emit(QtCore.SIGNAL('right_mouse_button_pressed'))

        else:
            return QtGui.QLabel.mousePressEvent(self, event)
