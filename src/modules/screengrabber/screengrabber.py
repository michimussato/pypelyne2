import datetime
import logging
import threading
import src.conf.SETTINGS as SETTINGS
from PyQt4 import QtGui, QtCore


class ScreenGrabber:
    def __init__(self):

        self.pixmap = QtGui.QPixmap
        self.pixmap_new = None
        self.pixmap_previous = None
        self.qimage = None
        self.thread = threading.Timer(1.0/SETTINGS.FPS, self.grab_screen)
        self.format = 'PNG'

        self.counter = 1

        self.now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')

        # self.start_capture()

    def start(self):
        self.grab_screen()
        self.counter += 1
        self.thread.start()

    def stop(self):
        self.thread.cancel()
        # self.thread = None

    def grab_screen(self):
        self.pixmap_new = self.pixmap.grabWindow(QtGui.QApplication.desktop().winId())
        self.qimage = self.pixmap_new.scaled(self.pixmap_new.size()*SETTINGS.SCALE_FACTOR,
                                             QtCore.Qt.KeepAspectRatio).toImage()

        if not self.pixmap_previous == self.pixmap_new:
            logging.debug('screengrab created.')
            self.pixmap_new.save('%s_screenshot_%s.%s' % (self.now,
                                                          str(self.counter).zfill(SETTINGS.PADDING),
                                                          self.format))
            # print 'captured'
        else:
            logging.debug('screengrab is equal to previous one. not saved.')

        self.pixmap_previous = self.pixmap_new
        

# import sys
# from PyQt4 import QtGui, QtCore
# import time
# import datetime
#
#
# fps = 2
# scale_factor = 0.5
# padding = 6
#
# app = QtGui.QApplication(sys.argv)
# old_qimage = None
# now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')
#
#
# for i in range(1, 10000):
#     print i
#     px = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
#     new_qimage = px.scaled(px.size()*scale_factor, QtCore.Qt.KeepAspectRatio).toImage()
#
#     if old_qimage == new_qimage:
#         print 'is equal to previous'
#     else:
#         new_qimage.save('%s_screenshot_%s.png' % (now, str(i).zfill(padding)), 'PNG')
#
#     old_qimage = new_qimage
#
#     time.sleep(1.0/fps)


# ex = Ui_MainWindow() #The class wher you call self.show()
# QPixmap.grabWidget(ex).save('screenshot.jpg', 'jpg')
