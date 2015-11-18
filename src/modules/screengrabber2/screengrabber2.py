import time
import sys
import os
import Queue
import datetime
import src.conf.SETTINGS as SETTINGS

from PyQt4 import QtGui, QtCore

# http://www.ifnamemain.com/posts/2014/Jul/11/screen_capture_1/


class Thread(QtCore.QThread):
    def __init__(self):
        super(Thread, self).__init__()
        self.halt = False
        self.queue = Queue.Queue()
        
    def run(self):
        fps = 1.0/SETTINGS.FPS
        while not self.halt:
            start_time = time.time()
            self.queue.put('capture')
            self.emit(QtCore.SIGNAL('capture()'))
            time_delta = time.time()-start_time
            wait = fps-time_delta
            if wait > 0:
                time.sleep(wait)
        
        # empty the queue here (thread safe)
        with self.queue.mutex:
            self.queue.queue.clear()
        

class ScreenGrabber(QtCore.QObject):
    def __init__(self):
        super(ScreenGrabber, self).__init__()
        self.now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')
        self.arrow = QtGui.QPixmap(SETTINGS.CURSOR_ICON).scaledToHeight(SETTINGS.CURSOR_SIZE)
        self.snap_shots = Thread()
        self.connect(self.snap_shots, QtCore.SIGNAL('capture()'), self.capture)
        self.capture_count = 0
        self.start_capture_time = None
        self.previous_px = None
        self.px = None
        self.px2 = None
        self.previous_image = None

    def start_capture(self):
        # time.sleep(0)
        self.capture_count = 0
        self.snap_shots.halt = False
        self.snap_shots.start()
        self.start_capture_time = time.time()
        
    def stop_capture(self):
        self.snap_shots.halt = True
        print 'stopped'

    def capture(self):
        # app.processEvents()

        print 'caught capture', 'tmp_{}_{}.{}'.format(self.now, str(self.capture_count).zfill(SETTINGS.PADDING), SETTINGS.GRABBER_FORMAT.lower(), SETTINGS.GRABBER_FORMAT)
        print 'current fps', float(self.capture_count)/(time.time()-self.start_capture_time)
        if not self.snap_shots.queue.empty():
            self.snap_shots.queue.get(0)

            self.px = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
            new_image = self.px.scaled(self.px.size()*SETTINGS.SCALE_FACTOR, QtCore.Qt.KeepAspectRatio).toImage()

            if not new_image == self.previous_image:
                if SETTINGS.CURSOR:
                    painter = QtGui.QPainter(new_image)
                    painter.drawPixmap(QtGui.QCursor.pos(), self.arrow)
                new_image.save('tmp_{}_{}.{}'.format(self.now, str(self.capture_count).zfill(SETTINGS.PADDING), SETTINGS.GRABBER_FORMAT).lower(), format=SETTINGS.GRABBER_FORMAT, quality=SETTINGS.GRABBER_QUALITY)
            else:
                print 'same image'
            self.previous_image = new_image
            self.capture_count += 1


if __name__ == '__main__':
    # global app
    app = QtGui.QApplication(sys.argv)
    
    window = ScreenGrabber()
    window.start_capture()
    # window.stop_capture()
    # time.sleep(4)
    # window.stop_capture()
    # window
    # window.show()
    sys.exit(app.exec_())
    # try:
    #     sys.exit(app.exec_())
    # except SystemExit as e:
    #     if e.code != 0:
    #         raise()
    #     os._exit(0)
