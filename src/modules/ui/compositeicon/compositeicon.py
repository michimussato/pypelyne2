import os
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
import src.conf.settings.SETTINGS as SETTINGS


class CompositeIcon(QtGui.QPixmap):
    def __init__(self, plugin=None, *__args):
        super(CompositeIcon, self).__init__()

    def set_icons(plugin):
        pixmap = QtGui.QPixmap(SETTINGS.PLUGINS_ICON_HEIGHT, SETTINGS.PLUGINS_ICON_HEIGHT)
        pixmap_hovered = QtGui.QPixmap(SETTINGS.PLUGINS_ICON_HEIGHT, SETTINGS.PLUGINS_ICON_HEIGHT)

        if plugin.architecture == 'x32':
            arch_icon = QtGui.QPixmap(SETTINGS.ICON_X32)
        elif plugin.architecture == 'x64':
            arch_icon = QtGui.QPixmap(SETTINGS.ICON_X64)

        if plugin.icon is None:
            icon = QtGui.QPixmap(SETTINGS.PLUGINS_DEFAULT_ICON)
        else:
            icon = QtGui.QPixmap(os.path.join(SETTINGS.PLUGINS_ICONS, plugin.icon))
        icon = icon.scaledToHeight(SETTINGS.PLUGINS_ICON_HEIGHT, QtCore.Qt.SmoothTransformation)

    def composite_icon(self):
        color = QtGui.QColor(0, 0, 0, 0)
        pixmap.fill(color)

        painter = QtGui.QPainter()
        painter.begin(pixmap)
        # http://doc.qt.io/qt-4.8/qpainter.html#CompositionMode-enum
        painter.setCompositionMode(painter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, icon)
        painter.drawPixmap(0, 0, arch_icon)
        painter.end()

    def composite_icon_hovered(self):
        color_hovered = QtGui.QColor(255, 255, 255, 255)
        self.pixmap_hovered.fill(color_hovered)

        painter_hovered = QtGui.QPainter()
        painter_hovered.begin(self.pixmap_hovered)
        painter_hovered.setCompositionMode(painter_hovered.CompositionMode_SourceOver)
        painter_hovered.drawPixmap(0, 0, self.pixmap_hovered)
        painter_hovered.drawPixmap(0, 0, self.pixmap)
        painter_hovered.end()
