# ui/minimap.py
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

class MinimapView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHints(self.renderHints() | QPainter.Antialiasing)
        self.setFixedSize(200, 150)
        # Scale the view down for a minimap effect.
        self.setTransform(self.transform().scale(0.1, 0.1))
        # Disable scrollbars.
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # We don't want users to move items in the minimap.
        self.setInteractive(False)
        # Pan callback that will be set by MainWindow.
        self.panCallback = None
        self._dragging = False

    def mousePressEvent(self, event):
        self._dragging = True
        scenePos = self.mapToScene(event.pos())
        if self.panCallback:
            self.panCallback(scenePos)
        event.accept()

    def mouseMoveEvent(self, event):
        if self._dragging:
            scenePos = self.mapToScene(event.pos())
            if self.panCallback:
                self.panCallback(scenePos)
        event.accept()

    def mouseReleaseEvent(self, event):
        self._dragging = False
        event.accept()
