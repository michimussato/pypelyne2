import os
import src.modules.psutil221 as psutil
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import src.conf.settings.SETTINGS as SETTINGS


class Worker(QtCore.QObject):
    def __init__(self, widget):
        super(Worker, self).__init__()
        self.widget = widget

    def update(self):
        self.update_cpu()
        self.update_mem()

    def update_mem(self):
        virtual_mem = psutil.virtual_memory()
        # print self.virtual_mem

        self.widget.mem.bar_item.setValue(int(virtual_mem.percent))
        self.widget.mem.label_item.setText('{0}/{1}MB'.format(str(int(float(virtual_mem.used)/1024/1024)),
                                                              str(int(float(virtual_mem.total)/1024/1024))))
        # threading.Timer(0.2, self.update).start()

    def update_cpu(self):
        cpu_times = psutil.cpu_percent(percpu=False)
        # print self.cpu_times
        self.widget.cpu.bar_item.setValue(cpu_times)
        self.widget.cpu.label_item.setText('{0}%'.format(str(int(cpu_times))))


class ResourceBarWidget(QtGui.QWidget):
    def __init__(self):
        super(ResourceBarWidget, self).__init__()

        self.cpu = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                           'src',
                                           'modules',
                                           'ui',
                                           'resourcebarwidget',
                                           'resourcebarwidget.ui'))
        self.mem = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                           'src',
                                           'modules',
                                           'ui',
                                           'resourcebarwidget',
                                           'resourcebarwidget.ui'))

        self.cpu.label_title.setText('CPU')
        self.cpu.label_item.setText('{0}%'.format('0'))
        self.mem.label_title.setText('Memory')
        self.mem.label_item.setText('{0}/{1}MB'.format('0', '0'))

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.cpu)
        self.layout.addWidget(self.mem)
        spacer = QtGui.QSpacerItem(1, 1, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout.addStretch()

        self.setLayout(self.layout)

        # self.cores = psutil.cpu_count(logical=True)

        # self.cpu_times = []
        self.timer = QtCore.QTimer()
        self.t = QtCore.QThread()
        self.worker = Worker(self)
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.worker.update)

        self.timer.start(SETTINGS.REFRESH_INTERVAL)

        self.worker.moveToThread(self.t)

        self.t.start()

    def closeEvent(self, event):
        self.timer.stop()
