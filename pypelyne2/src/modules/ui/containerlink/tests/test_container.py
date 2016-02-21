import sys
# import os
# import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
# import src.conf.settings.SETTINGS as SETTINGS
# import src.modules.ui.graphicsscene.graphicsscene as graphicsscene
import pypelyne2.src.modules.ui.graphicsview.graphicsview_stage as graphicsview_stage
# import pypelyne2.src.modules.ui.containerlink.container as container
import pypelyne2.src.modules.ui.mainwindow.mainwindow as mainwindow
# import pypelyne2.src.parser.parse_plugins as parse_plugins


app = QtGui.QApplication(sys.argv)

mainwindow = mainwindow.MainWindow()
# scene = QtGui.QGraphicsScene()
graphicssview_stage = graphicsview_stage.GraphicsViewStage()
# graphicssview_stage.setScene(scene)
# mainwindow.setCentralWidget(graphicssview_stage)

# container = container.ContainerLink(scene)

# scene.addItem(container)

mainwin = mainwindow
mainwin.show()
mainwin.raise_()
app.exec_()