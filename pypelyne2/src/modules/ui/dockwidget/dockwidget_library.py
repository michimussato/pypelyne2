# import PyQt4.QtGui as QtGui
# import PyQt4.QtCore as QtCore
# import pypelyne2.src.modules.ui.dockwidget.dockwidget as dockwidget
# # import pypelyne2.src.modules.ui.outputwidget.outputwidget as outputwidget
# # import pypelyne2.src.parser.parse_outputs as parse_outputs
#
#
# class DockWidgetOutputChannels(dockwidget.DockWidget):
#     def __init__(self, mainwindow=None):
#         super(DockWidgetOutputChannels, self).__init__()
#
#         self.mainwindow = mainwindow
#
#         self.setWindowTitle('Library')
#
#         self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
#         self.setFeatures(self.DockWidgetFloatable | self.DockWidgetMovable)
#
#         # self.outputs = parse_outputs.get_outputs()
#
#         self.library = get_library()
#
#         widget = QtGui.QWidget()
#         self.layout_library = QtGui.QVBoxLayout()
#
#         for library_item in self.library:
#             if library_item.item_enable:
#                 library_item_widget =
#                 self.layout_library.addWidget(library_item_widget)
#
#         widget.setLayout(self.layout_library)
#
#         scroll = QtGui.QScrollArea()
#         scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
#         scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
#         scroll.setWidgetResizable(False)
#         scroll.setWidget(widget)
#
#         container_layout = QtGui.QVBoxLayout()
#         container_layout.addWidget(scroll)
#         container_widget = QtGui.QWidget()
#         container_widget.setLayout(container_layout)
#         self.setWidget(container_widget)
