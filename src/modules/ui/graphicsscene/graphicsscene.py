import os
import cPickle
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic
import src.conf.settings.SETTINGS as SETTINGS


class GraphicsView(QtGui.QGraphicsView):
    def __init__(self, myView=[]):
        super(GraphicsView, self).__init__()
        # self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT, 'src', 'modules', 'graphicsscene', 'graphicsscene.ui'), self)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        # self.nodeView.wheelEvent = self.graphicsView_wheelEvent
        self.myView = myView

        self.setGeometry(600, 300, 600, 400)

        self.sc = GraphicsScene(parent=self)
        self.setScene(self.sc)

    # def wheelEvent(self, event):
    #     # 'zoom'
    #     sc = event.delta()/100
    #     if sc < 0:
    #         sc -= 1/sc
    #     self.myView.scale(sc, sc)
    #     self.myView.setDragMode(0)
    #     self.myView.showMatrix()


class GraphicsScene(QtGui.QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)
        self.addRect(30, 16, 20, 20, pen=QtGui.QPen(QtCore.Qt.blue))

    def dropEvent(self, event):
        if event.mimeData().hasFormat("application/x-imgname"):
            event.accept()
            data = event.mimeData().data("application/x-imgname")
            data = data.data()
            unPickleData = cPickle.loads(data)
            # unPickleData = userListModule.ListBaseClass.d[unPickleData]
            # Create the node in the scene
            self.createNode(unPickleData, event.scenePos())
            if unPickleData.dictKey is "emitterCat":
                newPos = event.scenePos()
                newPos.setY(newPos.y()-175)
                # behaviorNode = mayaNodesModule.MayaNodes['behaviorCat']
                # self.createNode(behaviorNode, newPos)

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-imgname"):
            event.accept()




#     def graphicsView_wheelEvent(self, event):
#
# #         numSteps = event.delta() / 15 / 8
# #
# #         if numSteps == 0:
# #             event.ignore()
# #
# #         sc = 1.25 * numSteps
# #         self.zoom(sc, self.mapToScene(event.pos()))
# #         event.accept()
#
#         factor = 1.15
#
#         #self.nodeView.centerOn()
#
#         #print 'event.delta() = %s' %event.delta()
#
#         if event.delta() > 0:
#             self.nodeView.scale(factor, factor)
#             self.nodeView.centerOn(event.pos())
#
#         else:
#             self.nodeView.scale(1.0 / factor, 1.0 / factor)
#             self.nodeView.centerOn(event.pos())


# '''Pan (left mouse but) and zoom (mouse wheel)  test'''
# '''Python 3.4 (No differance between PyQt4 and PyQt5)'''
# #from PyQt5 import QtGui, QtCore
# #import PyQt5.QtWidget as QW
# from PyQt4 import QtGui, QtCore
# import PyQt4.QtGui as QW
#
# import numpy as np
#
# class ZoomAndPan(QW.QGraphicsView):
#
#     def __init__(self,parent=None):
#         super(ZoomAndPan,self).__init__(parent)
#         self.setWindowTitle('ZoomAndPan')
#         self.setGeometry(600,300,600,400)
#         'Left button in top of image. Shows the transform matrix (press to reset)'
#         self.mess = QW.QPushButton('Transform Matrix\n\n\ndx,xy\ncounter', self)
#         self.mess.clicked.connect(self.resetM)
#
#         'm31 button, adds 200 to m31'
#         self.m31 = QW.QPushButton('m31', self)
#         self.m31.move(200,0)
#         self.m31.clicked.connect(self.addM31)
#
#         'm13 button, adds 0.0001 to m13'
#         self.m13 = QW.QPushButton('m13', self)
#         self.m13.move(300,0)
#         self.m13.clicked.connect(self.addM13)
#         self.count=0   #Counter
#
#         # Create scene
#         self.sc = scene(self,self)
#         self.setScene(self.sc)
#
#     def mouseMoveEvent(self,event):
#         'Pan by manipulting sceneRect'
#         pos=event.pos()
#         pos=self.mapToScene(pos)
#         dx=pos.x()-self.sc.startPos.x()
#         dy=pos.y()-self.sc.startPos.y()
#
#         rect=self.sceneRect().getRect()
#         self.setSceneRect(rect[0]-dx,rect[1]-dy,rect[2],rect[3])
#         # Increas counter to show that the loop works
#         self.count+=1
#         self.showMatrix()
#
#     def showMatrix(self):
#         'Show matrix in Textbox (Buttton)'
#         m=self.transform()
#         str1='{0:5.2f}{1:5.2f} {2:6.4f}\n'.format(m.m11(), m.m12(),m.m13())
#         str2='{0:5.2f}{1:5.2f}{2:5.2f}\n'.format(m.m21(), m.m22(),m.m23())
#         str3='{0:5.2f}{1:5.2f}{2:5.2f}\n'.format(m.m31(), m.m32(),m.m33())
#         str4='{0:5.2f}{1:5.2f}\n'.format(m.dx(), m.dy(),m.m33())
#         'Show counter '
#         str5='{0:5.0f}'.format(self.count)
#         self.mess.setText(str1+str2+str3+str4+str5)
#
#     def resetM(self):
#         'Reset transform'
#         self.resetTransform()
#         self.showMatrix()
#
#     def addM31(self):
#         'Add 200 to m31 '
#         m=self.transform()
#         m.setMatrix(m.m11(),m.m12(),m.m13(),m.m21(),m.m22(),m.m23(),m.m31()+200,m.m32(),m.m33())
#         self.setTransform(m)
#         self.showMatrix()
#
#     def addM13(self):
#         'Add 0.0001 to m13 '
#         m=self.transform()
#         m.setMatrix(m.m11(),m.m12(),m.m13()+0.0001,m.m21(),m.m22(),m.m23(),
#             m.m31(),m.m32(),m.m33())
#         self.setTransform(m)
#         self.showMatrix()
#
# class scene(QW.QGraphicsScene):
#     def __init__(self,parent,myView=[]):
#         QW.QGraphicsScene.__init__(self,parent)
#         self.myView=myView
#         # Some items in scene
#         self.txt=self.addSimpleText("///////")
#         self.txt.setPos(2,-20)
#         self.txt.setScale(2)
#         self.txt.setBrush(QtGui.QBrush(QtCore.Qt.green))
#         self.addRect(0,16,20,20, pen=QtGui.QPen(QtCore.Qt.blue))
#         self.addRect(10,60,32,8, pen=QtGui.QPen(QtCore.Qt.red))
#         self.addRect(30,16,20,20, pen=QtGui.QPen(QtCore.Qt.blue))
#         self.N=0
#
#     def mousePressEvent(self, event):
#         self.myView.setDragMode(1) # Works fine without this
#         self.startPos=event.scenePos()
#
#     def mouseReleaseEvent(self, event):
#         self.myView.setDragMode(0)
#
#     def wheelEvent(self, event):
#         'zoom'
#         sc=event.delta()/100
#         if sc<0: sc=-1/sc
#         self.myView.scale(sc,sc)
#         self.myView.setDragMode(0)
#         self.myView.showMatrix()
#


def main():
    app = QtGui.QApplication([])
    fig = GraphicsView()
    fig.show()
    app.exec_()


if __name__ == '__main__':
    main()
