import sys
from PyQt4 import QtGui, QtCore
import time
import datetime


fps = 2
scale_factor = 0.5
padding = 6

app = QtGui.QApplication(sys.argv)
old_qimage = None
now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M-%S')


for i in range(1, 10000):
    print i
    px = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())
    new_qimage = px.scaled(px.size()*scale_factor, QtCore.Qt.KeepAspectRatio).toImage()

    if old_qimage == new_qimage:
        print 'is equal to previous'
    else:
        new_qimage.save('%s_screenshot_%s.png' % (now, str(i).zfill(padding)), 'PNG')

    old_qimage = new_qimage

    time.sleep(1.0/fps)

# To get the App-Window use:
#
# ex = Ui_MainWindow() #The class wher you call self.show()
# QPixmap.grabWidget(ex).save('screenshot.jpg', 'jpg')
