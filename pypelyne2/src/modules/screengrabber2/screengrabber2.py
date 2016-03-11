import time
import logging
import sys
import Queue
import datetime
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore


# http://www.ifnamemain.com/posts/2014/Jul/11/screen_capture_1/


class Thread(QtCore.QThread):
    def __init__(self, screengrabber=None):
        super(Thread, self).__init__()
        self.screengrabber = screengrabber
        self.halt = False
        self.queue = Queue.Queue()
    #     self.connect(self.screengrabber, QtCore.SIGNAL('stop_capture()'), self.foo)

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
            logging.info('queue cleared')


class ScreenGrabber(QtCore.QObject):
    def __init__(self):
        super(ScreenGrabber, self).__init__()
        self.now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')
        self.arrow = QtGui.QPixmap(SETTINGS.CURSOR_ICON).scaledToHeight(SETTINGS.CURSOR_SIZE)
        self.snap_shots = Thread(self)
        self.connect(self.snap_shots, QtCore.SIGNAL('capture()'), self.capture)
        # self.connect(self.snap_shots, QtCore.SIGNAL('clicked()'), self.stop_capture)
        self.capture_count = 0
        if SETTINGS.TEST_MODE:
            self.loop = 0
        # self.start_capture_time = None
        self.capture_set = time.time()
        self.fps = SETTINGS.FPS
        self.previous_px = None
        self.px = None
        self.px2 = None
        self.previous_image = None

        # self.screen = QtCore.QScreenAppliction()
        #
        # print dir(self.screen)

    def start_capture(self):
        if SETTINGS.TEST_MODE:
            self.loop = 0
        self.snap_shots.halt = False
        if self.capture_count == 0:
            logging.info('starting capture')
        else:
            logging.info('continuing capture')
        self.snap_shots.start()

    def stop_capture(self):
        self.snap_shots.halt = True
        self.emit(QtCore.SIGNAL('stop_capture()'))
        self.snap_shots.quit()
        logging.info('stopped')

    def capture(self):
        # app.processEvents()

        # if SETTINGS.TEST_MODE:
        #     loop = 0

        # self.fps =

        if time.time() == self.capture_set:

            self.capture_count += 1

            return

        logging.info('caught capture (tmp_{0}_{1}.{2})'.format(self.now,
                                                               str(self.capture_count+1).zfill(SETTINGS.PADDING),
                                                               SETTINGS.GRABBER_FORMAT.lower(),
                                                               SETTINGS.GRABBER_FORMAT))

        logging.info('current fps: {0}'.format(self.fps))

        if not self.snap_shots.queue.empty():
            self.snap_shots.queue.get(0)

            # http://www.qtforum.org/article/26719/how-to-screen-capture-of-secondary-screen-and-display.html

            screen = QtGui.QApplication.desktop()
            window_id = screen.winId()

            self.px = QtGui.QPixmap.grabWindow(window_id, screen.x(), screen.y(), screen.width(), screen.height())

            screen_rect = self.px.rect()

            if SETTINGS.CURSOR:

                painter = QtGui.QPainter(self.px)

                cursor_point = QtCore.QPoint(QtGui.QCursor.pos().x()-screen.x(), QtGui.QCursor.pos().y()-screen.y())

                painter.drawPixmap(cursor_point, self.arrow)

            new_image = self.px.scaled(self.px.size()*SETTINGS.SCALE_FACTOR,
                                       QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.SmoothTransformation).toImage()

            if not new_image == self.previous_image or not SETTINGS.ENABLE_SKIP_IDENTICAL:

                if SETTINGS.TEXT_OVERLAY:

                    painter = QtGui.QPainter()

                    painter.begin(new_image)

                    ###############
                    # box

                    pen_rects = QtGui.QPen(QtGui.QColor(255, 0, 0, 255))
                    brush_rects = QtGui.QBrush(QtGui.QColor(128, 128, 128, 100))

                    painter.setPen(pen_rects)
                    painter.setBrush(brush_rects)

                    mask_rect = QtCore.QRect()

                    mask_rect_height = 200

                    mask_rect.setRect(0, screen_rect.height()*SETTINGS.SCALE_FACTOR-mask_rect_height, screen_rect.width()*SETTINGS.SCALE_FACTOR-1, mask_rect_height-1)

                    painter.drawRect(mask_rect)
                    ###############

                    # https://doc.qt.io/archives/qtjambi-4.5.2_01/com/trolltech/qt/gui/QPainter.CompositionMode.html
                    # painter.setCompositionMode(painter.CompositionMode_SourceIn)
                    # painter.setCompositionMode(painter.CompositionMode_Difference)

                    if bool(SETTINGS.TEXT_OVERLAY_COMPOSITION_MODE):

                        painter.setCompositionMode(SETTINGS.TEXT_OVERLAY_COMPOSITION_MODE)

                    painter.setPen(SETTINGS.TEXT_OVERLAY_COLOR)

                    font = QtGui.QFont()

                    # font.setStyleStrategy(font.ForceOutline)

                    font.setFamily(SETTINGS.TEXT_OVERLAY_FONT)

                    font.setPointSize(SETTINGS.TEXT_OVERLAY_SIZE)
                    painter.setFont(font)

                    text_fps = painter.drawText(QtCore.QRectF(0, 0, new_image.width(), new_image.height()),
                                                QtCore.Qt.AlignLeft,
                                                str('recording@{0}/{1}fps'.format(round(self.fps, 2), SETTINGS.FPS)))


                    painter.end()

                new_image.save('tmp_{0}_{1}.{2}'.format(self.now,
                                                        str(self.capture_count+1).zfill(SETTINGS.PADDING),
                                                        SETTINGS.GRABBER_FORMAT).lower(),
                               format=SETTINGS.GRABBER_FORMAT,
                               quality=SETTINGS.GRABBER_QUALITY)

            else:
                logging.info('same image like previous one. not saved.')
            self.previous_image = new_image

            if SETTINGS.TEST_MODE:
                self.loop += 1
                if self.loop == SETTINGS.TEST_TIME * SETTINGS.FPS:
                    self.stop_capture()
                    if SETTINGS.TEST_LOOP:

                        self.start_capture()

            self.capture_count += 1

            self.fps = float(self.capture_count)/(time.time() - self.capture_set)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    window = ScreenGrabber()
    window.start_capture()

    sys.exit(app.exec_())
