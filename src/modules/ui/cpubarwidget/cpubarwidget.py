import os
import src.modules.psutil221 as psutil
import PyQt4.QtGui as QtGui
# import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import src.conf.settings.SETTINGS as SETTINGS
import threading


class CpuBarWidget(QtGui.QWidget):
    def __init__(self):
        super(CpuBarWidget, self).__init__()

        self.cpu = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT, 'src', 'modules', 'ui', 'cpubarwidget', 'cpubarwidget.ui'))
        self.mem = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT, 'src', 'modules', 'ui', 'cpubarwidget', 'cpubarwidget.ui'))

        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.cpu)
        self.layout.addWidget(self.mem)

        self.setLayout(self.layout)

        self.cores = psutil.cpu_count(logical=True)

        self.cpu_times = []

        self.cpu_times = None

        self.update()

    def update(self):
        self.update_cpu()
        self.update_mem()
        threading.Timer(0.1, self.update).start()

    def update_mem(self):
        self.virtual_mem = psutil.virtual_memory()
        # print self.virtual_mem

        self.mem.bar_item.setValue(int(self.virtual_mem.percent))
        self.mem.label_item.setText('{0}/{1}MB'.format(str(int(float(self.virtual_mem.used)/1024/1024)), str(int(float(self.virtual_mem.total)/1024/1024))))
        # threading.Timer(0.2, self.update).start()

    def update_cpu(self):
        self.cpu_times = psutil.cpu_percent(interval=2, percpu=False)
        # print self.cpu_times
        self.cpu.bar_item.setValue(self.cpu_times)
        self.cpu.label_item.setText('{0}%'.format(str(int(self.cpu_times))))
