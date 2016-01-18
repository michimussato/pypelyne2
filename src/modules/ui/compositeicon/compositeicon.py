import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import src.conf.settings.SETTINGS as SETTINGS


class ExpandCollapse(QtGui.QPixmap):
    def __init__(self):
        super(ExpandCollapse, self).__init__()



class CompositeIcon(QtGui.QPixmap):
    def __init__(self, plugin=None, *__args):
        super(CompositeIcon, self).__init__()

        self.plugin = plugin

        if self.plugin.icon is None:
            icon = QtGui.QPixmap(SETTINGS.PLUGINS_DEFAULT_ICON)
        else:
            icon = QtGui.QPixmap(self.plugin.icon)
        self._icon = icon.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT, QtCore.Qt.SmoothTransformation)

        self._pixmap = QtGui.QPixmap(SETTINGS.PLUGINS_ICON_HEIGHT, SETTINGS.PLUGINS_ICON_HEIGHT)

        # print self.plugin.type
        # print self.plugin.family

        self.lock_icon = QtGui.QPixmap(SETTINGS.ICON_LOCKED).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT,
                                                                           QtCore.Qt.SmoothTransformation)

        self.maximize_icon = QtGui.QPixmap(SETTINGS.ICON_MAXIMIZE).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT,
                                                                           QtCore.Qt.SmoothTransformation)

        self.expand_icon = QtGui.QPixmap(SETTINGS.ICON_EXPAND).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT*SETTINGS.ICON_SCALE,
                                                                              QtCore.Qt.SmoothTransformation)

        self.collapse_icon = QtGui.QPixmap(SETTINGS.ICON_COLLAPSE).scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT*SETTINGS.ICON_SCALE,
                                                                                  QtCore.Qt.SmoothTransformation)

        if self.plugin.type == 'submitter':
            self.overlay_icon = QtGui.QPixmap(SETTINGS.ICON_SUBMITTER)
        elif self.plugin.type == 'plugin':
            pass
            # TODO: plugin
            # self.overlay_icon = QtGui.QPixmap(SETTINGS.ICON_PLUGIN)
        elif self.plugin.type == 'standalone':
            if self.plugin.architecture_agnostic:
                self.overlay_icon = QtGui.QPixmap(SETTINGS.ICON_AGNOSTIC)
            else:
                if self.plugin.architecture == 'x32':
                    self.overlay_icon = QtGui.QPixmap(SETTINGS.ICON_X32)
                elif self.plugin.architecture == 'x64':
                    self.overlay_icon = QtGui.QPixmap(SETTINGS.ICON_X64)
        self.overlay_icon = self.overlay_icon.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT,
                                                             QtCore.Qt.SmoothTransformation)

    @property
    def lock(self):
        return self.lock_icon

    @property
    def maximize(self):
        return self.maximize_icon

    @property
    def expand(self):
        return self.expand_icon

    @property
    def collapse(self):
        return self.collapse_icon

    @property
    def pixmap_overlay(self):
        color = QtGui.QColor(0, 0, 0, 0)
        _pixmap = self._pixmap
        _pixmap.fill(color)

        painter = QtGui.QPainter()
        painter.begin(_pixmap)
        painter.drawPixmap(0, 0, self._icon)
        painter.setCompositionMode(painter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, self.overlay_icon.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT / 2.5,
                                                                  QtCore.Qt.SmoothTransformation))
        painter.end()

        return _pixmap

    @property
    def pixmap_hovered(self):
        color_hovered = QtGui.QColor(0, 0, 0, 0)
        _pixmap_hovered = self._icon.alphaChannel()
        _pixmap_hovered.fill(color_hovered)

        painter_hovered = QtGui.QPainter()
        painter_hovered.begin(_pixmap_hovered)
        painter_hovered.drawPixmap(0, 0, self.overlay_icon.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT / 2.5,
                                                                          QtCore.Qt.SmoothTransformation))
        painter_hovered.setCompositionMode(painter_hovered.CompositionMode_SourceOver)
        painter_hovered.drawPixmap(0, 0, self._icon)
        painter_hovered.end()

        return _pixmap_hovered

    @property
    def pixmap_no_overlay(self):
        return self._icon

    @property
    def arch_icon(self):
        return self.overlay_icon
