import datetime
import logging
import sys
# import threading
import src.conf.SETTINGS as SETTINGS
from PyQt4 import QtGui, QtCore


class ScreenGrabber(QtCore.QThread):
    def __init__(self):
        super(ScreenGrabber, self).__init__()

        self.timer = QtCore.QTimer()

        self.timer.setSingleShot(False)
        self.previous_image = None
        self.pixmap_previous = None
        self.qimage = None
        self.format = 'PNG'

        self.counter = 1

        self.now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')

        self.timer = QtCore.QTimer(self)

        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.grab_screen)

        self.timer.start(1000.0/SETTINGS.FPS)

        # self.run()

    # def stop(self):
    #     self.timer.stop()

    def grab_screen(self):
        px = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
        new_image = px.scaled(px.size()*SETTINGS.SCALE_FACTOR, QtCore.Qt.KeepAspectRatio).toImage()

        if not new_image == self.previous_image:

            logging.debug('screengrab created.')
            new_image.save('%s_screenshot_%s.%s' % (self.now,
                                                    str(self.counter).zfill(SETTINGS.PADDING),
                                                    SETTINGS.GRABBER_FORMAT.lower()),
                           format=SETTINGS.GRABBER_FORMAT,
                           quality=SETTINGS.GRABBER_QUALITY)
        else:
            logging.debug('screengrab is equal to previous one. not saved.')

        self.previous_image = new_image

        self.counter += 1


app = QtGui.QApplication(sys.argv)
test = ScreenGrabber()
# test.run()

app.exec_()
# test.quit()
