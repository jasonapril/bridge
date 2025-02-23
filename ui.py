from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string("""
<!doctype html>
<html>
  <head>
    <title>Neural Net Web UI</title>
    <style>
      html, body { margin: 0; padding: 0; height: 100%; overflow: hidden; background: #2e2e2e; }
      #mainCanvas {
        position: absolute; top: 0; left: 0;
        width: 100%; height: 100%;
        background: #2e2e2e;
      }
      .node {
        position: absolute;
        width: 120px;
        height: 60px;
        background: #262626;
        color: #ffffff;
        border: 1px solid #ffffff;
        border-radius: 4px;
        cursor: move;
        user-select: none;
        text-align: center;
        line-height: 60px;
      }
      #minimap {
        position: absolute;
        top: 10px;
        right: 10px;
        width: 200px;
        height: 150px;
        background: #1a1a1a;
        border: 1px solid cyan;
        z-index: 1000;
      }
      #controls {
        position: absolute;
        top: 170px;
        right: 10px;
        background: rgba(42, 42, 42, 0.9);
        padding: 10px;
        border: 1px solid #ffffff;
        color: #ffffff;
        z-index: 1000;
      }
      button {
        background: #3e3e3e;
        color: #ffffff;
        border: none;
        padding: 8px;
        margin: 4px 0;
        cursor: pointer;
      }
      button:hover { background: #575757; }
    </style>
  </head>
  <body>
    <!-- The main canvas for drawing the grid -->
    <canvas id="mainCanvas"></canvas>
    
    <!-- Floating minimap in the upper-right -->
    <canvas id="minimap"></canvas>
    
    <!-- Floating control panel below the minimap -->
    <div id="controls">
      <button onclick="runNetwork()">Run Network</button>
      <button onclick="loadPreset()">Load Bell Curve Preset</button>
      <button onclick="addLayer()">Add Layer</button>
    </div>
    
    <!-- Example nodes -->
    <div id="inputNode" class="node" style="left: 100px; top: 100px;">Input</div>
    <div id="hidden1" class="node" style="left: 300px; top: 200px;">Layer 1</div>
    <div id="outputNode" class="node" style="left: 500px; top: 100px;">Output Graph</div>
    
    <script>
      // Resize the main canvas to fill the window
      var mainCanvas = document.getElementById("mainCanvas");
      var ctx = mainCanvas.getContext("2d");
      function resizeCanvas() {
        mainCanvas.width = window.innerWidth;
        mainCanvas.height = window.innerHeight;
        drawGrid();
      }
      window.addEventListener("resize", resizeCanvas);
      resizeCanvas();
      
      // Draw a subtle grid on the main canvas
      function drawGrid() {
        var spacing = 100;
        ctx.clearRect(0, 0, mainCanvas.width, mainCanvas.height);
        ctx.strokeStyle = "#444444";
        for (var x = 0; x < mainCanvas.width; x += spacing) {
          ctx.beginPath();
          ctx.moveTo(x, 0);
          ctx.lineTo(x, mainCanvas.height);
          ctx.stroke();
        }
        for (var y = 0; y < mainCanvas.height; y += spacing) {
          ctx.beginPath();
          ctx.moveTo(0, y);
          ctx.lineTo(mainCanvas.width, y);
          ctx.stroke();
        }
      }
      
      // Basic draggable node implementation
      function makeDraggable(el) {
        var pos = {x: 0, y: 0};
        el.onmousedown = dragMouseDown;
        function dragMouseDown(e) {
          e = e || window.event;
          e.preventDefault();
          pos.x = e.clientX;
          pos.y = e.clientY;
          document.onmouseup = closeDragElement;
          document.onmousemove = elementDrag;
        }
        function elementDrag(e) {
          e = e || window.event;
          e.preventDefault();
          var dx = pos.x - e.clientX;
          var dy = pos.y - e.clientY;
          pos.x = e.clientX;
          pos.y = e.clientY;
          el.style.top = (el.offsetTop - dy) + "px";
          el.style.left = (el.offsetLeft - dx) + "px";
        }
        function closeDragElement() {
          document.onmouseup = null;
          document.onmousemove = null;
        }
      }
      
      // Make our example nodes draggable
      makeDraggable(document.getElementById("inputNode"));
      makeDraggable(document.getElementById("hidden1"));
      makeDraggable(document.getElementById("outputNode"));
      
      // Setup minimap (for demonstration, the minimap is a simple scaled version of the main canvas)
      var minimap = document.getElementById("minimap");
      var mctx = minimap.getContext("2d");
      function updateMinimap() {
        mctx.clearRect(0, 0, minimap.width, minimap.height);
        // For simplicity, we just draw the grid scaled down
        var scale = 0.1;
        mctx.strokeStyle = "cyan";
        for (var x = 0; x < minimap.width; x += 10) {
          mctx.beginPath();
          mctx.moveTo(x, 0);
          mctx.lineTo(x, minimap.height);
          mctx.stroke();
        }
        for (var y = 0; y < minimap.height; y += 10) {
          mctx.beginPath();
          mctx.moveTo(0, y);
          mctx.lineTo(minimap.width, y);
          mctx.stroke();
        }
      }
      updateMinimap();
      
      // Allow clicking and dragging on the minimap to pan the main canvas
      minimap.onmousedown = function(e) {
        panFromMinimap(e);
        minimap.onmousemove = panFromMinimap;
        document.onmouseup = function() {
          minimap.onmousemove = null;
        };
      };
      function panFromMinimap(e) {
        var rect = minimap.getBoundingClientRect();
        var clickX = e.clientX - rect.left;
        var clickY = e.clientY - rect.top;
        // Compute target offset (this is a simplified example)
        var targetX = clickX * 10 - window.innerWidth / 2;
        var targetY = clickY * 10 - window.innerHeight / 2;
        window.scrollTo(targetX, targetY);
      }
      
      // Dummy functions for controls (to be replaced with real neural net logic)
      function runNetwork() {
        alert("Running network... (this is a stub)");
      }
      function loadPreset() {
        alert("Loading bell curve preset... (this is a stub)");
      }
      function addLayer() {
        var id = "layer" + (document.getElementsByClassName("node").length);
        var node = document.createElement("div");
        node.className = "node";
        node.id = id;
        node.innerHTML = "New Layer";
        node.style.left = "400px";
        node.style.top = "300px";
        document.body.appendChild(node);
        makeDraggable(node);
      }
    </script>
  </body>
</html>
    """)

if __name__ == "__main__":
    # In your notebook, you can comment out app.run(), since your nn.py is already loaded.
    app.run(debug=True)
