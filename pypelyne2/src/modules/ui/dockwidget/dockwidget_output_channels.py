import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

import pypelyne2.src.modules.core.parser.parse_outputs as parse_outputs
import pypelyne2.src.modules.ui.dockwidget.dockwidget as dockwidget
import pypelyne2.src.modules.ui.outputwidget.outputwidget as outputwidget


class DockWidgetOutputChannels(dockwidget.DockWidget):
    def __init__(self, mainwindow=None):
        super(DockWidgetOutputChannels, self).__init__()

        self.mainwindow = mainwindow

        self.setWindowTitle('Outputs')

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)

        self.outputs = parse_outputs.get_outputs()

        widget = QtGui.QWidget()
        self.layout_outputs = QtGui.QVBoxLayout()

        for output in self.outputs:
            if output.output_enable:
                plugin_widget = outputwidget.OutputWidget(output=output, mainwindow=mainwindow)
                self.layout_outputs.addWidget(plugin_widget)

        widget.setLayout(self.layout_outputs)

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
