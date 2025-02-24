# ui/mainwindow.py
from PySide6.QtWidgets import QMainWindow, QDockWidget, QToolBar, QPushButton, QGraphicsScene
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt
from ui.zoomableview import ZoomableView
from ui.node_item import NodeItem
from ui.minimap import MinimapView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neural Net Qt UI")
        self.resize(1200, 800)
        
        # Create the scene and the zoomable view (our main canvas).
        self.scene = QGraphicsScene(-5000, -5000, 10000, 10000)
        self.view = ZoomableView(self.scene)
        self.setCentralWidget(self.view)
        
        # Draw grid lines on the scene.
        self.drawGrid()
        
        # Add some example nodes.
        self.createExampleNodes()
        
        # Create the minimap and set its pan callback.
        self.minimap = MinimapView(self.scene)
        self.minimap.panCallback = lambda scenePos: self.view.centerOn(scenePos)
        dock = QDockWidget("Minimap", self)
        dock.setWidget(self.minimap)
        # Disable the close button.
        dock.setFeatures(QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        
        # Create a toolbar for controls.
        toolbar = QToolBar("Controls", self)
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        addLayerBtn = QPushButton("Add Layer")
        addLayerBtn.clicked.connect(self.addLayer)
        runBtn = QPushButton("Run Network")
        runBtn.clicked.connect(self.runNetwork)
        presetBtn = QPushButton("Load Preset")
        presetBtn.clicked.connect(self.loadPreset)
        toolbar.addWidget(addLayerBtn)
        toolbar.addWidget(runBtn)
        toolbar.addWidget(presetBtn)
    
    def drawGrid(self):
        pen = QPen(Qt.gray)
        spacing = 100
        for x in range(-5000, 5000, spacing):
            self.scene.addLine(x, -5000, x, 5000, pen)
        for y in range(-5000, 5000, spacing):
            self.scene.addLine(-5000, y, 5000, y, pen)
    
    def createExampleNodes(self):
        inputNode = NodeItem("Input", 100, 100)
        self.scene.addItem(inputNode)
        layer1 = NodeItem("Layer 1", 300, 200)
        self.scene.addItem(layer1)
        outputNode = NodeItem("Output Graph", 500, 100)
        self.scene.addItem(outputNode)
    
    def addLayer(self):
        layerCount = sum(1 for item in self.scene.items() if isinstance(item, NodeItem) and item.label.startswith("Layer"))
        newLayer = NodeItem(f"Layer {layerCount+1}", 400, 300)
        self.scene.addItem(newLayer)
    
    def runNetwork(self):
        # For demonstration, update the output node's label with a dummy value.
        for item in self.scene.items():
            if isinstance(item, NodeItem) and item.label.startswith("Output"):
                item.setText("Output: 3.14")
    
    def loadPreset(self):
        # Placeholder for preset functionality.
        print("Preset loaded.")
