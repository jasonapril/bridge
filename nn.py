# nn.py
import numpy as np

class NodeModel:
    def __init__(self, node_type, x, y, data=None):
        """
        node_type: e.g. "input", "layer", "output", "control"
        x, y: initial position on the canvas
        data: dictionary holding node-specific parameters (for neural net computations)
        """
        self.node_type = node_type  
        self.x = x
        self.y = y
        self.data = data or {}      

# Activation functions used in the neural net computations.
def linear(x):
    return x

def sigmoid(x):
    return 1/(1+np.exp(-x))

def tanh(x):
    return np.tanh(x)

def relu(x):
    return np.maximum(0, x)

activation_functions = {
    "linear": linear,
    "sigmoid": sigmoid,
    "tanh": tanh,
    "relu": relu,
}
