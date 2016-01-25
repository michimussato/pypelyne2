from PyQt4 import QtGui, QtCore

class WiringGraphicsView(QtGui.QGraphicsView):
    #Initializer method
    def __init__(self, parent = None,  scene=None):
        QtGui.QGraphicsView.__init__(self, scene, parent)
    #Set Accept Drops property true
        self.setAcceptDrops(True)

    #This method creates a line between two widgets
    def paintWire(self, start_widget,  end_widget):
        #Size and Position of both widgets
        _start = start_widget.geometry()
        _end = end_widget.geometry()
        #Creates a Brush object with Red color
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0) )
        #Creates Pen object with specified brush
        pen = QtGui.QPen(brush, 2)
        #Create a Line object between two widgets
        line = QtGui.QGraphicsLineItem(_start.x() + _start.width() / 2, _start.y() + _start.height() / 2, _end.x() + _end.width() / 2, _end.y() + _end.height() / 2)
        #Set the Pen for the Line
        line.setPen(pen)
        #Add this line item to the scene.
        self.scene().addItem( line )

class DragButton(QtGui.QPushButton):
    def __init__(self, parent):
         super(DragButton,  self).__init__(parent)
         self.allowDrag = True

    def setAllowDrag(self, allowDrag):
        if type(allowDrag) == bool:
           self.allowDrag = allowDrag
        else:
            raise TypeError("You have to set a boolean type")

    def mouseMoveEvent(self, e):
        if e.buttons() != QtCore.Qt.RightButton:
            return QtGui.QPushButton.mouseMoveEvent(self, e)

        if self.allowDrag == True:
            # write the relative cursor position to mime data
            mimeData = QtCore.QMimeData()
            # simple string with 'x,y'
            mimeData.setText('%d,%d' % (e.x(), e.y()))
            # print mimeData.text()

            # let's make it fancy. we'll show a "ghost" of the button as we drag
            # grab the button to a pixmap
            pixmap = QtGui.QPixmap.grabWidget(self)

            # below makes the pixmap half transparent
            painter = QtGui.QPainter(pixmap)
            painter.setCompositionMode(painter.CompositionMode_DestinationIn)
            painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
            painter.end()

            # make a QDrag
            drag = QtGui.QDrag(self)
            # put our MimeData
            drag.setMimeData(mimeData)
            # set its Pixmap
            drag.setPixmap(pixmap)
            # shift the Pixmap so that it coincides with the cursor position
            drag.setHotSpot(e.pos())

            # start the drag operation
            # exec_ will return the accepted action from dropEvent
            if drag.exec_(QtCore.Qt.LinkAction | QtCore.Qt.MoveAction) == QtCore.Qt.LinkAction:
                print 'linked'
            else:
                print 'moved'

        return QtGui.QPushButton.mouseMoveEvent(self, e)

    def mousePressEvent(self, e):

        if e.button() == QtCore.Qt.LeftButton:
            print 'press'
            #AQUI DEBO IMPLEMENTAR EL MENU CONTEXTUAL
        return QtGui.QPushButton.mousePressEvent(self, e)

    def dragEnterEvent(self, e):
        e.accept()
        return QtGui.QPushButton.dragEnterEvent(self, e)

    def dropEvent(self, e):
        # get the relative position from the mime data
        mime = e.mimeData().text()
        x, y = map(int, mime.split(','))
            # move
            # so move the dragged button (i.e. event.source())
        print e.pos()
        # e.source().move(e.pos()-QtCore.QPoint(x, y))
            # set the drop action as LinkAction
        e.setDropAction(QtCore.Qt.LinkAction)
        # tell the QDrag we accepted it
        e.accept()

        return QtGui.QPushButton.dropEvent(self, QDropEvent(QPoint(e.pos().x(), e.pos().y()), e.possibleActions(), e.mimeData(), e.buttons(), e.modifiers()))



from PyQt4.QtGui import *
from PyQt4.QtCore import *

class MyScene(QGraphicsScene):
    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        # find item at these coordinates
        item = self.itemAt(e.scenePos())
        if item.setAcceptDrops == True:
            # pass on event to item at the coordinates
            try:
               item.dropEvent(e)
            except RuntimeError:
                pass #This will supress a Runtime Error generated when dropping into a widget with no ProxyWidget

    def dragMoveEvent(self, e):
        e.acceptProposedAction()

class MyProxy(QGraphicsProxyWidget):
    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        # pass drop event to child widget
        return self.widget().dropEvent(e)

    def dragMoveEvent(self, e):
        e.acceptProposedAction()


app = QApplication([])

scene = MyScene()

menu = QMenu()

# put a button into the scene and move it
button1 = DragButton('Button 1')
button1.setText("aaa")
button1.setDefault(False)
button1.setAutoDefault(True)
#button1.setMouseTracking(True)
button1.setAllowDrag(True) #Allow Drag n Drop of DragButton
button1.setGeometry(QRect(50, 50, 51, 31)) #Set dimensions of it
#Set icon of button1
icon = QIcon()
icon.addPixmap(QPixmap(":/audio-input-line.png"), QIcon.Normal, QIcon.Off)
button1.setIcon(icon)
button1.setFlat(True)
button1.setMenu(menu)
#Create a QGraphicsProxyWidget adding the widget to scene
scene_button1 = scene.addWidget(button1)
#move the button on the scene
r1 = scene_button1.geometry()
r1.moveTo(-100, -50)

# put another button into the scene
button2 = DragButton('Button 2')
button2.setText("bbb")
#This button shoudn't be dragged, it is just for dropping.
button2.setAllowDrag(False)
button2.setAcceptDrops(True)
icon = QIcon()
icon.addPixmap(QPixmap(":/input_small.png"), QIcon.Normal, QIcon.Off)
button2.setIcon(icon)
#button2.setMouseTracking(True)
#button2.setGeometry(QRect(270, 150, 41, 31))

# Instantiate our own proxy which forwars drag/drop events to the child widget
my_proxy = MyProxy()
my_proxy.setWidget(button2)
my_proxy.setAcceptDrops(True)
scene.addItem(my_proxy)

# Create the view using the scene
view = WiringGraphicsView(None, scene)
view.resize(300, 200)
view.show()
#and paint a wire between those buttons
view.paintWire(button1, button2)
app.exec_()