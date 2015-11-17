import datetime
import logging
import sys
# import threading
import src.conf.SETTINGS as SETTINGS
from PyQt4 import QtGui, QtCore


class ScreenGrabber(QtCore.QThread):
    def __init__(self):
        super(ScreenGrabber, self).__init__()

        # self.thread = QtCore.QThread()
        # self.thread.run()

        self.timer = QtCore.QTimer()
        # self.timer.moveToThread(self.thread)

        self.timer.setSingleShot(False)
        # self.timer.timeout.connect(self.grab_screen)
        # self.timer.connect(self.grab_screen)

        self.pixmap = QtGui.QPixmap
        self.pixmap_new = None
        self.pixmap_previous = None
        self.qimage = None
        # self.thread = threading.Timer(1.0/SETTINGS.FPS, self.grab_screen)
        self.format = 'PNG'

        self.counter = 1

        self.now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')

        self.timer = QtCore.QTimer(self)

        # self.connect(self, QtCore.SIGNAL('stop()'), self.stop())
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.grab_screen)

        self.timer.start(1000.0/SETTINGS.FPS)

        self.run()
        # self.quit()

    # def run(self):
    #     self.timer.start(1000.0/SETTINGS.FPS)

    # def quit(self):
    #     self.timer.stop()

    def stop(self):
        self.timer.stop()

    def grab_screen(self):
        print 'jeasdf'
        self.pixmap_new = self.pixmap.grabWindow(QtGui.QApplication.desktop().winId())
        self.qimage = self.pixmap_new.scaled(self.pixmap_new.size()*SETTINGS.SCALE_FACTOR,
                                             QtCore.Qt.KeepAspectRatio).toImage()

        if not self.pixmap_previous == self.pixmap_new:
            logging.debug('screengrab created.')
            self.pixmap_new.save('%s_screenshot_%s.%s' % (self.now,
                                                          str(self.counter).zfill(SETTINGS.PADDING),
                                                          self.format))
            # logging.debug('screengrab created.')
            # self.pixmap_new.save('%s.%s' % (str(self.counter).zfill(SETTINGS.PADDING),
            #                                 self.format))
            # print 'captured'
        else:
            logging.debug('screengrab is equal to previous one. not saved.')

        self.pixmap_previous = self.pixmap_new

        self.counter += 1

        # self.timer.stop()
        # self.quit()

    #     # self.thread = QtCore.QThread()
    #     # self.thread.run()
    #
    #     self.timer = QtCore.QTimer()
    #     # self.timer.moveToThread(self.thread)
    #
    #     self.timer.setSingleShot(False)
    #     self.timer.timeout.connect(self.grab_screen)
    #     # self.timer.connect(self.grab_screen)
    #
    #     self.pixmap = QtGui.QPixmap
    #     self.pixmap_new = None
    #     self.pixmap_previous = None
    #     self.qimage = None
    #     # self.thread = threading.Timer(1.0/SETTINGS.FPS, self.grab_screen)
    #     self.format = 'PNG'
    #
    #     self.counter = 1
    #
    #     self.now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')
    #
    #     # self.grab_screen()
    #
    #     # self.timer.start(1.0/SETTINGS.FPS)
    #
    #     self.run()
    #
    # def run(self):
    #     # self.thread.run()
    #     self.timer.start(1.0/SETTINGS.FPS)
    #
    # def stop(self):
    #     self.timer.stop()
    #
    # def grab_screen(self):
    #     print 'jeasdf'
    #     self.pixmap_new = self.pixmap.grabWindow(QtGui.QApplication.desktop().winId())
    #     self.qimage = self.pixmap_new.scaled(self.pixmap_new.size()*SETTINGS.SCALE_FACTOR,
    #                                          QtCore.Qt.KeepAspectRatio).toImage()
    #
    #     if not self.pixmap_previous == self.pixmap_new:
    #         logging.debug('screengrab created.')
    #         self.pixmap_new.save('%s_screenshot_%s.%s' % (self.now,
    #                                                       str(self.counter).zfill(SETTINGS.PADDING),
    #                                                       self.format))
    #         # print 'captured'
    #     else:
    #         logging.debug('screengrab is equal to previous one. not saved.')
    #
    #     self.pixmap_previous = self.pixmap_new


app = QtGui.QApplication(sys.argv)
test = ScreenGrabber()
test.run()

app.exec_()
# test.stop()
        

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
