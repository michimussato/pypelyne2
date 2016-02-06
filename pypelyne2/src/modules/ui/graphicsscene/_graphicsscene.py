import cPickle
import logging
import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import pypelyne2.src.modules.ui.nodeui.nodeui as nodeui
import pypelyne2.src.modules.nodecore.nodecore as nodecore
import pypelyne2.src.modules.ui.container.container as container
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


# class DraggableMark(QtGui.QGraphicsItem):
#     def __init__(self, position, scene):
#         super(DraggableMark, self).__init__(None, scene)
#         self.setFlags(QtGui.QGraphicsItem.ItemIsSelectable | QtGui.QGraphicsItem.ItemIsMovable)
#
#         self.rect = QtCore.QRectF()
#         self.setPos(position)
#         scene.clearSelection()
#
#     def boundingRect(self):
#         return self.rect
#
#     def paint(self, painter, option, widget):
#         painter.setRenderHint(QtGui.QPainter.Antialiasing)
#         pen = QtGui.QPen(QtCore.Qt.SolidLine)
#         pen.setColor(QtCore.Qt.black)
#         pen.setWidth(3)
#
#         if option.state & QtGui.QStyle.State_Selected:
#             pen.setColor(QtCore.Qt.green)
#         painter.setPen(pen)
#         painter.setBrush(QtGui.QColor(200, 0, 0))
#         painter.drawRoundedRect(self.rect, 10.0, 10.0)
#
#
#
#

