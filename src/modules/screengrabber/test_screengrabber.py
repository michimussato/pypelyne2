import src.modules.screengrabber.screengrabber as screengrabber
import time
import sys
import PyQt4.QtGui as QtGui


app = QtGui.QApplication(sys.argv)
# global app
# app = QApplication(sys.argv)
grabber = screengrabber.ScreenGrabber()
# app.exec_()


# grabber.run()
#
# time.sleep(60)
#
# grabber.stop()
