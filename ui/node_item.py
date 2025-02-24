# ui/node_item.py
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PySide6.QtGui import QBrush, QPen
from PySide6.QtCore import QRectF, Qt

class NodeItem(QGraphicsRectItem):
    def __init__(self, label, x, y, width=120, height=60):
        super().__init__(0, 0, width, height)
        self.setBrush(QBrush(Qt.darkGray))
        self.setPen(QPen(Qt.white))
        self.setFlags(QGraphicsRectItem.ItemIsMovable | QGraphicsRectItem.ItemIsSelectable)
        self.label = label
        self.textItem = QGraphicsTextItem(label, self)
        self.textItem.setDefaultTextColor(Qt.white)
        rect = QRectF(0, 0, width, height)
        self.textItem.setTextWidth(rect.width())
        self.textItem.setPos(0, (rect.height() - self.textItem.boundingRect().height()) / 2)
        self.setPos(x, y)
    
    def setText(self, newText):
        self.label = newText
        self.textItem.setPlainText(newText)
