import src.modules.screengrabber.screengrabber as screengrabber
import time
import sys
import PyQt4.QtGui as QtGui


# app = QtGui.QApplication(sys.argv)

grabber = screengrabber.ScreenGrabber()
grabber.start()

time.sleep(60)

grabber.stop()
