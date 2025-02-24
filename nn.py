# nn.py
import numpy as np

def linear(x):
    return x

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

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

def run_network(x_values, layers_config):
    """
    A dummy feedforward pass.
    layers_config should be a list of dictionaries, each representing a layer.
    Each layer should have an 'activation' and a list of 'neurons', where each neuron has 'weights' and 'bias'.
    """
    activations = x_values
    for layer in layers_config:
        act = activation_functions.get(layer.get("activation", "linear"), linear)
        outputs = []
        for neuron in layer.get("neurons", []):
            weights = np.array(neuron.get("weights", [1.0] * activations.shape[1]))
            bias = neuron.get("bias", 0.0)
            z = np.dot(activations, weights) + bias
            outputs.append(act(z))
        if outputs:
            activations = np.column_stack(outputs)
    return activations
