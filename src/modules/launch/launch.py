import PyQt4.QtCore as QtCore


class Launch(QtCore.QProcess):
    def __init__(self, plugin=None,):
        super(Launch).__init__()
        self.plugin = plugin

    def launch_instance_x32(self, plugin=None):
        process = QtCore.QProcess(self)
        process.started.connect(self.started)
        process.finished.connect(self.finished)
        process.start(plugin.executable_x32, plugin.flags_x32)

    def launch_instance_x64(self, plugin=None):
        process = QtCore.QProcess(self)
        process.started.connect(self.started)
        process.finished.connect(self.finished)
        process.start(plugin.executable_x64, plugin.flags_x64)

    def started(self):
        print 'started'

    def finished(self):
        print 'finished'
