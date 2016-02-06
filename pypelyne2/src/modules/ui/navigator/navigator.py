import PyQt4.QtGui as QtGui
import pypelyne2.src.conf.settings.SETTINGS as SETTINGS


class Navigator(QtGui.QGraphicsItem):
    def __init__(self, scene_object=None, view_object=None):
        super(Navigator, self).__init__()

        self.scene_object = scene_object
        self.view_object = view_object

        if SETTINGS.ENABLE_NAVIGATOR:
            self.screen_representation = QtGui.QGraphicsRectItem(0,
                                                                 0,
                                                                 self.scene_object.itemsBoundingRect().width() * SETTINGS.NAVIGATOR_SCALE,
                                                                 self.scene_object.itemsBoundingRect().height() * SETTINGS.NAVIGATOR_SCALE)

            self.scene_object.addItem(self.screen_representation)

            self.screen_representation.setZValue(1000.0)

            self.scene_representation = QtGui.QGraphicsRectItem(0,
                                                                0,
                                                                self.scene_object.itemsBoundingRect().width() * SETTINGS.NAVIGATOR_SCALE,
                                                                self.scene_object.itemsBoundingRect().height() * SETTINGS.NAVIGATOR_SCALE)

            self.scene_object.addItem(self.scene_representation)
            self.scene_representation.setZValue(1000.0)
            self.screen_representation.setParentItem(self.scene_representation)

            color_navigator_rect = QtGui.QColor(SETTINGS.NAVIGATOR_R*255,
                                                SETTINGS.NAVIGATOR_G*255,
                                                SETTINGS.NAVIGATOR_B*255,
                                                SETTINGS.NAVIGATOR_ALPHA*255)
            color_screen_rect = QtGui.QColor(255-SETTINGS.NAVIGATOR_R*255,
                                             255-SETTINGS.NAVIGATOR_G*255,
                                             255-SETTINGS.NAVIGATOR_B*255,
                                             SETTINGS.NAVIGATOR_ALPHA*255)
            brush_navigator_rect = QtGui.QBrush(color_screen_rect)
            brush_screen_rect = QtGui.QBrush(color_navigator_rect)
            self.screen_representation.setBrush(brush_navigator_rect)
            self.scene_representation.setBrush(brush_screen_rect)

        else:
            return

    def adjust_navigator(self):
        if SETTINGS.ENABLE_NAVIGATOR:

            # if self.sceneRect().width()*SETTINGS.NAVIGATOR_MAX_SIZE < self.scene_representation.rect().width():
            #     print 'too wide'
            # if self.sceneRect().height()*SETTINGS.NAVIGATOR_MAX_SIZE < self.scene_representation.rect().height():
            #     print 'too tall'

            self.screen_representation.setRect(0,
                                               0,
                                               self.view_object.viewport().width() * SETTINGS.NAVIGATOR_SCALE,
                                               self.view_object.viewport().height() * SETTINGS.NAVIGATOR_SCALE)

            # self.screen_representation.setRect(0,
            #                                    0,
            #                                    self.scene.itemsBoundingRect().width() * SETTINGS.NAVIGATOR_SCALE,
            #                                    self.scene.itemsBoundingRect().height() * SETTINGS.NAVIGATOR_SCALE)

            # magic function:
            relative_rect = self.mapFromScene(self.scene_object.itemsBoundingRect()).boundingRect()
            # print relative_rect.topLeft()
            # print relative_rect.bottomLeft()
            # print relative_rect.topRight()
            # print relative_rect.bottomRight()

            self.scene_representation.setRect(relative_rect.x() * SETTINGS.NAVIGATOR_SCALE,
                                              relative_rect.y() * SETTINGS.NAVIGATOR_SCALE,
                                              relative_rect.width() * SETTINGS.NAVIGATOR_SCALE,
                                              relative_rect.height() * SETTINGS.NAVIGATOR_SCALE)

            self.scene_representation.setPos(self.view_object.viewport().width() - self.scene_representation.rect().width() - self.scene_representation.rect().topLeft().x(),
                                             self.view_object.viewport().height() - self.scene_representation.rect().height() - self.scene_representation.rect().topLeft().y())

            if self.scene_representation.rect().width()-self.screen_representation.rect().width() > 1.0\
                    or self.scene_representation.rect().height()-self.screen_representation.rect().height() > 1.0:
                self.scene_representation.setVisible(True)
            else:
                self.scene_representation.setVisible(False)

        else:
            return
