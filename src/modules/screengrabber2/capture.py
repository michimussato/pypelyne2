'''
capture.py

A simple screen capture app using PySide ( or PyQt4 )

#TODO: modifications required to run on Windows

Copyright Marc Robinson 2014

'''

import time
import sys,os
import threading
import Queue
import numpy

from PyQt4.QtGui import QPixmap, QApplication, QMainWindow,QWidget,\
                        QPushButton,QVBoxLayout,QPainter,QCursor,QSpinBox,\
                        QLabel,QGridLayout,QLineEdit,QButtonGroup,QRadioButton, \
                        QGroupBox,QLayout

from PyQt4.QtCore import SIGNAL,Qt, QThread

class SelectedArea(QWidget):
    def __init__(self):
        QWidget.__init__(self,None,Qt.Window)
        
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint  | Qt.X11BypassWindowManagerHint | Qt.FramelessWindowHint )
        self.setStyleSheet("QWidget { background-color: rgba(255, 192, 64, 50%); \
                                      border: 1px solid rgb(255, 192, 64)}")

class TransWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self,None,Qt.Window)
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.showMaximized()
        self.activateWindow()
        self.raise_()
        self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint  | Qt.X11BypassWindowManagerHint \
                            | Qt.FramelessWindowHint )
        
        screenGeometry = QApplication.desktop().availableGeometry();
        self.setGeometry(screenGeometry)
        self.setStyleSheet("QWidget { background-color: rgba(255,255,255, 5%); }")
    
    def mousePressEvent(self, QMouseEvent):
        self.hide()
        xd = QApplication.desktop().screenGeometry().x() - QApplication.desktop().availableGeometry().x()
        yd = QApplication.desktop().screenGeometry().y() - QApplication.desktop().availableGeometry().y()
        self.pos = numpy.array([QMouseEvent.pos().x()-xd,
                               QMouseEvent.pos().y()-yd])
        self.emit(SIGNAL("mouse_press()"))
    
class SnapShots(QThread):
    def __init__(self,main_window,fps=25):
        QThread.__init__(self)
        self.fps = fps
        self.main_window = main_window
        self.halt = False
        self.queue = Queue.Queue()
        
    def run(self,fps=None):
        if(fps!=None):self.fps=fps
        period = 1.0/self.fps
        print self.halt,  not (self.halt)
        while not (self.halt):
            st = time.time()
            while not self.queue.empty():
                pass
            self.queue.put("capture")
            self.emit(SIGNAL("capture()"))
            td = time.time()-st
            wait = period-td
            #print td
            if(wait>0):time.sleep(wait)
        
        #empty the queue here (thread safe)    
        with self.queue.mutex:
            self.queue.queue.clear()
        
class OptionsContainer(QWidget):
    def __init__(self,main_window):
        QWidget.__init__(self)
        self.main_window = main_window
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        self.lr = numpy.zeros(2)
        
        self.fps = QSpinBox()
        self.fps.setValue(25)
        self.fps.setMinimum(1)
        self.fps.setMaximum(1000)
        self.layout.addWidget(QLabel("FPS:"),10,10)
        self.layout.addWidget(self.fps,10,11)
        
        self.capture_area_group = QButtonGroup()
        self.capture_area_fs = QRadioButton("Full Screen")
        self.connect(self.capture_area_fs, SIGNAL("clicked()"),self.capture_area_change)
        self.capture_area_fs.setChecked(True)
        self.capture_area_sa = QRadioButton("Selected Area")
        self.connect(self.capture_area_sa, SIGNAL("clicked()"),self.capture_area_change)
        self.capture_area_group.addButton(self.capture_area_fs)
        self.capture_area_group.addButton(self.capture_area_sa)
        self.capture_area_group.setExclusive(True)
        
        self.layout.addWidget(self.capture_area_fs,12,10)
        self.layout.addWidget(self.capture_area_sa,12,11)
        
        self.sa_group = QGroupBox()
        self.sa_grid = QGridLayout()
        self.sa_group.setLayout(self.sa_grid)
        
        
        self.sa_ul_bt = QPushButton("Select Upper Left")
        self.connect(self.sa_ul_bt, SIGNAL("clicked()"), self.select_ul)
        self.sa_lr_bt = QPushButton("Select Lower Right")
        self.connect(self.sa_lr_bt, SIGNAL("clicked()"), self.select_lr)

        self.sa_x = QSpinBox()
        self.sa_y = QSpinBox()
        self.sa_w = QSpinBox()
        self.sa_h = QSpinBox()
        for sb in [self.sa_h,self.sa_w,self.sa_x,self.sa_y]:
            sb.setMaximum(999999)
            sb.setMinimum(0)
        
        self.sa_grid.addWidget(self.sa_ul_bt,14,10,1,1)
        self.sa_grid.addWidget(self.sa_lr_bt,15,10,1,1)
        self.sa_grid.addWidget(QLabel("x"),14,11,1,1)
        self.sa_grid.addWidget(self.sa_x,14,12,1,1)
        self.sa_grid.addWidget(QLabel("y"),15,11,1,1)
        self.sa_grid.addWidget(self.sa_y,15,12,1,1)
        self.sa_grid.addWidget(QLabel("w"),16,11,1,1)
        self.sa_grid.addWidget(self.sa_w,16,12,1,1)
        self.sa_grid.addWidget(QLabel("h"),17,11,1,1)
        self.sa_grid.addWidget(self.sa_h,17,12,1,1)
        
        self.sa_show_bt = QPushButton("Show Area")
        self.sa_show_bt.setCheckable(True)
        self.connect(self.sa_show_bt, SIGNAL("clicked()"), self.show_selected_area)

        
        self.sa_grid.addWidget(self.sa_show_bt,18,10,1,10)
        
        self.sa_group.hide()
        
        self.layout.addWidget(self.sa_group,14,10,1,10)
        
        self.capture_delay = QSpinBox()
        self.capture_delay.setMinimum(0)
        self.capture_delay.setMaximum(10000)
        
        self.layout.addWidget(QLabel("Capture Delay"),18,10,1,1)
        self.layout.addWidget(self.capture_delay,18,11,1,1)
        
        self.capture_bt = QPushButton("Capture")
        self.stop_capture_bt = QPushButton("Stop")
        self.stop_capture_bt.hide()
        self.layout.addWidget(self.capture_bt,20,10,1,10)
        self.layout.addWidget(self.stop_capture_bt,30,10,1,10)
        
        self.ffmpeg_flags = QLineEdit()
        self.ffmpeg_flags.setText("-qscale 0 -vcodec mpeg4")
        self.layout.addWidget(QLabel("FFMPEG Flags:"),40,10)
        self.layout.addWidget(self.ffmpeg_flags,50,10,1,10)
        
        self.encode_bt = QPushButton("Encode Video")
        self.layout.addWidget(self.encode_bt,60,10,1,10)
        
        self.open_dir_bt = QPushButton("Open Directory")
        self.layout.addWidget(self.open_dir_bt,80,10,1,10)
        
        self.connect(self.open_dir_bt, SIGNAL("clicked()"),self.open_cwd)
    
        self.selected_area = SelectedArea()
    
    def show_selected_area(self):
        x = self.sa_x.value()
        y = self.sa_y.value()
        w = self.sa_w.value()
        h = self.sa_h.value()
        
        self.selected_area.setGeometry(x,y,w,h)
        self.selected_area.activateWindow()
        self.selected_area.raise_()
        if(self.sa_show_bt.isChecked()):
            self.selected_area.show()
        else:self.selected_area.hide()
        
    def select_ul(self):
        print "select_ul"
        self.clicked  = False
        self.tw = TransWindow()
        self.tw.mouse_press = False
        self.tw.show()
        
        self.connect(self.tw, SIGNAL("mouse_press()"),self.set_ul)
        
    def select_lr(self):
        print "select_lr"
        self.clicked  = False
        self.tw = TransWindow()
        self.tw.mouse_press = False
        self.tw.show()
        
        self.connect(self.tw, SIGNAL("mouse_press()"),self.set_lr)
    
    def set_ul(self):
        self.sa_x.setValue( self.tw.pos[0])       
        self.sa_y.setValue( self.tw.pos[1])
        self.sa_w.setValue( self.lr[0] - self.sa_x.value())       
        self.sa_h.setValue( self.lr[1] - self.sa_y.value())
        self.show_selected_area()
        
    
    def set_lr(self):
        self.lr = numpy.array([self.tw.pos[0],self.tw.pos[1]])
        self.sa_w.setValue( self.tw.pos[0] - self.sa_x.value())       
        self.sa_h.setValue( self.tw.pos[1] - self.sa_y.value())     
        self.show_selected_area()
        
    
    def capture_area_change(self):
        print "capture_area_change"
        if(self.capture_area_fs.isChecked()):
            self.sa_group.hide()
        else:
            self.sa_group.show()
            
        self.adjustSize()
        self.main_window.adjustSize()
    
    def open_cwd(self):
        #will need to detect os and change accordingly
        os.system("open {}".format(os.getcwd()))
    
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self,None,Qt.WindowStaysOnTopHint)
        self.options = OptionsContainer(self)
        self.setCentralWidget(self.options)
        
        self.arrow_icon = os.path.abspath(os.path.dirname(__file__)+"/cursor3.png")
        print "self.arrow_icon",self.arrow_icon
    
        self.fmt = "08d"
        self.v_ext = "mp4"
        self.ffmpeg_bin = "ffmpeg"
    
        self.connect(self.options.capture_bt, SIGNAL("clicked()"),self.start_capture)
        self.connect(self.options.stop_capture_bt, SIGNAL("clicked()"),self.stop_capture)
        self.connect(self.options.encode_bt, SIGNAL("clicked()"),self.encode_video)
        
        self.snap_shots = SnapShots(self,fps = self.options.fps.value())
        
        self.connect(self.snap_shots, SIGNAL("capture()"),self.capture)

    def remove_all_snap_shots(self):
        try:os.system("rm tmp_*.jpg")
        except:pass
    
    def start_capture(self):
        
        time.sleep(self.options.capture_delay.value())
        self.UID = numpy.random.randint(0,9999999)
        self.remove_all_snap_shots()
        self.capture_count = 0
        self.snap_shots.halt=False
        self.snap_shots.fps =   self.options.fps.value()
        self.snap_shots.start()
        self.options.capture_bt.hide()
        self.options.encode_bt.setEnabled(False)
        self.options.stop_capture_bt.show()
        self.start_capture_time = time.time()
        
    def stop_capture(self):
        self.snap_shots.halt=True
        #self.snap_shots.wait()
        self.options.stop_capture_bt.hide()
        self.options.capture_bt.show()
        self.options.encode_bt.setEnabled(True)
        self.stop_capture_time = time.time()
        print "stopped"
        
    def capture(self):
        app.processEvents()

        print "caught capture",('tmp_{}_{:'+self.fmt+'}.jpg').format(self.UID,self.capture_count)
        print "current fps",float(self.capture_count)/(time.time()-self.start_capture_time)
        if not self.snap_shots.queue.empty():
            self.snap_shots.queue.get(0)
            arrow = QPixmap(self.arrow_icon);
            self.px = QPixmap.grabWindow(QApplication.desktop().winId())
            painter = QPainter(self.px)
            painter.drawPixmap(QCursor.pos(), arrow)
            if(self.options.capture_area_sa.isChecked()):
                self.px2 = self.px.copy(self.options.sa_x.value(),
                                        self.options.sa_y.value(),
                                        self.options.sa_w.value(),
                                        self.options.sa_h.value())
            else:
                self.px2 = self.px
            self.px2.save(('tmp_{}_{:'+self.fmt+'}.jpg').format(self.UID,self.capture_count), 'jpg')
            self.capture_count+=1

     
    def encode_video(self):
        fprefix = ('tmp_{}_').format(self.UID)
        fps=int(float(self.capture_count)/(self.stop_capture_time-self.start_capture_time))
        #fps = self.options.fps.value()
        vidfile = "screenshot_{}_video.{}".format(self.UID,self.v_ext)
        systemcall = str(self.ffmpeg_bin)+" -r " + str(fps) + " -y "
        systemcall += " -i " + str(fprefix)+"%"+str(self.fmt)+".jpg"
        systemcall += " "+str(self.options.ffmpeg_flags.text())
        systemcall += " "+str(vidfile)
        print systemcall
        os.system(systemcall) 
    
    def mousePressEvent(self, QMouseEvent):
        print QMouseEvent.pos()
        
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            sys.exit()
        
if __name__ == '__main__':
    global app
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    try:
        sys.exit(app.exec_())
    except SystemExit as e:
        if e.code != 0:
            raise()
        os._exit(0)

