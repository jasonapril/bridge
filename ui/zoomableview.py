# ui/zoomableview.py
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

class ZoomableView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self._zoom = 0
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
    
    def wheelEvent(self, event):
        zoomInFactor = 1.15
        zoomOutFactor = 1 / zoomInFactor
        if event.angleDelta().y() > 0:
            factor = zoomInFactor
            self._zoom += 1
        else:
            factor = zoomOutFactor
            self._zoom -= 1
        # Limit zoom level.
        if self._zoom < -10:
            self._zoom = -10
            return
        if self._zoom > 20:
            self._zoom = 20
            return
        self.scale(factor, factor)
