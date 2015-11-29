import src.modules.screengrabber.screengrabber as screengrabber
import sys
import PyQt4.QtGui as QtGui


app = QtGui.QApplication(sys.argv)
grabber = screengrabber.ScreenGrabber()
# app.exec_()
