import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.modules.ui.dockwidget.dockwidget as dockwidget
# import pypelyne2.src.modules.ui.pluginwidget.pluginwidget as pluginwidget
import pypelyne2.src.modules.ui.containerwidget.containerwidget as containerwidget

import pypelyne2.src.parser.parse_containers as parse_containers
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class DockWidgetContainers(dockwidget.DockWidget):
    def __init__(self, mainwindow=None):
        super(DockWidgetContainers, self).__init__()

        self.mainwindow = mainwindow

        self.setWindowTitle('Containers')

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self.containers = parse_containers.get_containers()

        widget = QtGui.QWidget()
        self.layout_containers = QtGui.QVBoxLayout()

        for container in self.containers:
            if container.container_enable:
                container_widget = containerwidget.ContainerWidget(container=container, mainwindow=mainwindow)
                self.layout_containers.addWidget(container_widget)

        widget.setLayout(self.layout_containers)

        scroll = QtGui.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(False)
        scroll.setWidget(widget)

        container_layout = QtGui.QVBoxLayout()
        container_layout.addWidget(scroll)
        container_widget = QtGui.QWidget()
        container_widget.setLayout(container_layout)
        self.setWidget(container_widget)
