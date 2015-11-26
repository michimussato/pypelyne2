# import PyQt4.QtGui as QtGui
# import PyQt4.QtCore as QtCore

import src.modules.ui.graphicsview.graphicsview as graphicsview
import src.modules.ui.graphicsscene.graphicsscene as graphicsscene
# import src.modules.ui.rectangle.rectangle as rectangle



class GraphicsViewStage(graphicsview.GraphicsView):
    def __init__(self):
        super(GraphicsViewStage, self).__init__()
        self.scene = graphicsscene.GraphicsScene()
        self.setScene(self.scene)
        # self.setResizeAnchor(self.AnchorUnderMouse)
        # self.setSceneRect(0, 0, 500, 500)

        # self.resize(self.scene.width(), self.scene.height())
        # self.setCentralWidget(self.view)
        # self.setAcceptDrops(True)
        # self.rectangle = rectangle.Rectangle()
        # self.scene.addItem(self.rectangle)

    def wheelEvent(self, event):

        # numSteps = event.delta() / 15 / 8
        #
        # if numSteps == 0:
        #     event.ignore()
        #
        # sc = 1.25 * numSteps
        # self.zoom(sc, self.mapToScene(event.pos()))
        # event.accept()

        # delta = 2 * (event.pos().x())
        # self.setResizeAnchor(self.AnchorViewCenter)
        self.setResizeAnchor(self.AnchorUnderMouse)
        factor = 1.15

        # print self.visibleRegion().boundingRect()

        # for i in dir(self):
        #     if not i.startswith('_'):
        #         print i, getattr(self, i)


        # print self.x()
        # print self.y()
        # print event.pos()
        # print self.frameRect()
        # print self.frameSize()
        print ''
        visible_rect = self.mapToScene(self.rect()).boundingRect()
        self.setSceneRect(visible_rect)
        print self.sceneRect()
        print visible_rect
        # print self.mapFromScene(self.mapToScene(self.rect()).boundingRect()).boundingRect()
        print self.mapToScene(event.pos())

        #self.nodeView.centerOn()

        #print 'event.delta() = %s' %event.delta()

        if event.delta() > 0:
            self.scale(factor, factor)
            # self.centerOn()
            # self.centerOn(self.mapToScene(event.pos()))

        else:
            self.scale(1.0 / factor, 1.0 / factor)
            # self.centerOn(self.mapToScene(event.pos()))

        # self.setResizeAnchor(self.AnchorUnderMouse)


