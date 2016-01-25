import sys
import PyQt4.QtGui as QtGui
import src.modules.ui.player.player as player


app = QtGui.QApplication(sys.argv)
# screen_size = QtGui.QApplication.desktop().availableGeometry()
scene = player.Player()
scene.add_player()
# scene.resize(int(screen_size.width()), int(screen_size.height()))
scene.show()
app.exec_()
