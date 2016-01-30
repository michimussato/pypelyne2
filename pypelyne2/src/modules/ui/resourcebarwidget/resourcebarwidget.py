import os
import psutil
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class Communicate(QtCore.QObject):
    updateBW = QtCore.pyqtSignal(int)


class BurningWidget(QtGui.QWidget):
    def __init__(self, max_value, monitor_item):
        super(BurningWidget, self).__init__()

        self.value = 0
        self.num = []

        self.monitor_item = monitor_item

        self.maximum = float(max_value)
        self.increment = self.maximum/SETTINGS.SECTION_COUNT

        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(1, 17)

        for i in range(SETTINGS.SECTION_COUNT):
            self.num.append(self.increment*(i+1))

    def set_value(self, value):
        self.value = value

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_widget(qp)
        qp.end()

    def draw_widget(self, qp):
        font = QtGui.QFont('Serif', 7, QtGui.QFont.Light)
        qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()

        step = int(round(w / float(SETTINGS.SECTION_COUNT)))

        threshold_mid = self.maximum * SETTINGS.THRESHOLD_MID
        threshold_high = self.maximum * SETTINGS.THRESHOLD_HIGH

        normal = int(((w / self.maximum) * self.value))
        # mid = int((w / self.maximum) * threshold_mid)
        # high = int(((w / self.maximum) * threshold_high))

        if self.value >= threshold_high:
            qp.setPen(SETTINGS.COLOR_TEXT)
            qp.setBrush(SETTINGS.COLOR_HIGH)
            qp.drawRect(0, 0, normal, h)

        elif self.value >= threshold_mid:
            qp.setPen(SETTINGS.COLOR_TEXT)
            qp.setBrush(SETTINGS.COLOR_MID)
            qp.drawRect(0, 0, normal, h)

        else:
            qp.setPen(SETTINGS.COLOR_TEXT)
            qp.setBrush(SETTINGS.COLOR_LOW)
            qp.drawRect(0, 0, normal, h)

        pen = QtGui.QPen(SETTINGS.COLOR_TEXT, 1, QtCore.Qt.SolidLine)

        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w-1, h-1)

        j = 0

        try:
            for i in range(step, SETTINGS.SECTION_COUNT*step, step):
                qp.drawLine(i, 0, i, 1)
                metrics = qp.fontMetrics()
                fw = metrics.width(str(self.num[j]))
                if i == step:
                    qp.drawText(i-fw/2, h/2, str(self.monitor_item))
                else:
                    qp.drawText(i-fw/2, h/2, str(int(self.num[j])))
                j += 1

        except ValueError, e:
            # TODO: something meaningful here
            print e


class Worker(QtCore.QObject):
    def __init__(self, widget, monitor_item):
        super(Worker, self).__init__()
        self.monitor_item = monitor_item
        self.widget = widget

    def update(self):
        if str(self.monitor_item).startswith('cpu'):
            self.update_cpu()
        elif str(self.monitor_item).startswith('mem'):
            self.update_mem()
        elif str(self.monitor_item).startswith('dsk'):
            self.update_dsk()
        elif str(self.monitor_item).startswith('net'):
            self.update_net()

    def update_mem(self):
        virtual_mem = psutil.virtual_memory()

        current_mem = int(float(virtual_mem.used)/1024/1024/SETTINGS.MEM_MULT)

        self.widget.c.updateBW.emit(current_mem)
        self.widget.repaint()

    def update_cpu(self):
        cpu_times = psutil.cpu_percent(percpu=False)

        self.widget.c.updateBW.emit(cpu_times)
        self.widget.repaint()

    def update_dsk(self):
        disks = psutil.disk_partitions(all=False)
        used = int(float(psutil.disk_usage(disks[0].mountpoint).used)/1024/1024/1024)
        self.widget.c.updateBW.emit(used)
        self.widget.repaint()

    def update_net(self):
        pass


class NodeBarWidget(QtGui.QWidget):
    def __init__(self, monitor_item, maximum):
        super(NodeBarWidget, self).__init__()

        self.c = None
        self.wid = None
        self.layout = QtGui.QVBoxLayout()

        self.monitor_item = monitor_item

        self.maximum = maximum

        self.c = Communicate()
        self.wid = BurningWidget(self.maximum, self.monitor_item)
        self.c.updateBW[int].connect(self.wid.set_value)

        self.layout.addWidget(self.wid)

        self.setLayout(self.layout)

        self.timer = QtCore.QTimer()
        self.t = QtCore.QThread()
        self.worker = Worker(self, self.monitor_item)
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.worker.update)

        self.timer.start(SETTINGS.REFRESH_INTERVAL)

        self.worker.moveToThread(self.t)

        self.t.start()

    def closeEvent(self, event):
        self.timer.stop()


class BarWidget(QtGui.QWidget):
    def __init__(self, monitor_item, maximum):
        super(BarWidget, self).__init__()

        self.c = None
        self.wid = None
        self.layout = QtGui.QVBoxLayout()

        self.monitor_item = monitor_item

        self.maximum = maximum

        self.c = Communicate()
        self.wid = BurningWidget(self.maximum, self.monitor_item)
        self.c.updateBW[int].connect(self.wid.set_value)

        self.layout.addWidget(self.wid)

        self.setLayout(self.layout)

        self.timer = QtCore.QTimer()
        self.t = QtCore.QThread()
        self.worker = Worker(self, self.monitor_item)
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.worker.update)

        self.timer.start(SETTINGS.REFRESH_INTERVAL)

        self.worker.moveToThread(self.t)

        self.t.start()

    def closeEvent(self, event):
        self.timer.stop()


class ResourceBarWidget(QtGui.QWidget):
    def __init__(self):
        super(ResourceBarWidget, self).__init__()

        self.layout = QtGui.QVBoxLayout()

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT,
                                          'src',
                                          'modules',
                                          'ui',
                                          'resourcebarwidget',
                                          'resourcebarwidget.ui'))

        self.scroll_layout = QtGui.QVBoxLayout()
        spacer = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)

        if SETTINGS.ENABLE_CPU:
            widget = QtGui.QWidget()
            label = QtGui.QLabel('')
            label.setFixedWidth(SETTINGS.ICON_HEIGHT)
            layout = QtGui.QHBoxLayout()
            pixmap = QtGui.QPixmap(os.path.join(SETTINGS.ICONS_DIR, 'cpu.png')).scaledToHeight(SETTINGS.ICON_HEIGHT, QtCore.Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            layout.addWidget(label)
            # layout.addItem(spacer)
            self.cpu_bar = BarWidget(monitor_item='cpu', maximum=100)
            layout.addWidget(self.cpu_bar)
            widget.setLayout(layout)
            self.ui.scroll_layout.addWidget(widget)

        if SETTINGS.ENABLE_MEM:
            widget = QtGui.QWidget()
            label = QtGui.QLabel('')
            label.setFixedWidth(SETTINGS.ICON_HEIGHT)
            layout = QtGui.QHBoxLayout()
            pixmap = QtGui.QPixmap(os.path.join(SETTINGS.ICONS_DIR, 'mem.png')).scaledToHeight(SETTINGS.ICON_HEIGHT, QtCore.Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            layout.addWidget(label)

            self.mem_bar = BarWidget(monitor_item='mem', maximum=SETTINGS.TOTAL_MEM/SETTINGS.MEM_MULT)
            layout.addWidget(self.mem_bar)
            widget.setLayout(layout)
            self.ui.scroll_layout.addWidget(widget)

        if SETTINGS.ENABLE_DSK:
            widget = QtGui.QWidget()
            label = QtGui.QLabel('')
            label.setFixedWidth(SETTINGS.ICON_HEIGHT)
            layout = QtGui.QHBoxLayout()
            pixmap = QtGui.QPixmap(os.path.join(SETTINGS.ICONS_DIR, 'dsk.png')).scaledToHeight(SETTINGS.ICON_HEIGHT, QtCore.Qt.SmoothTransformation)
            label.setPixmap(pixmap)
            layout.addWidget(label)
            self.dsk_bar = BarWidget(monitor_item='dsk', maximum=SETTINGS.TOTAL_DSK)
            layout.addWidget(self.dsk_bar)
            widget.setLayout(layout)
            self.ui.scroll_layout.addWidget(widget)

        # nets = psutil.net_connections()

        # for disk in self.disks:
        #     print disk.mountpoint
        #     # print dir(disk)
        #     # print dir(psutil.disk_usage(disk.mountpoint))
        #     total = psutil.disk_usage(disk.mountpoint).total
        #     used = psutil.disk_usage(disk.mountpoint).used
        #     print used, total

        self.ui.scroll_layout.addItem(spacer)

        self.layout.addWidget(self.ui)

        self.setLayout(self.layout)
