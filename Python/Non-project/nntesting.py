import numpy as np

class NN_Node:
    def __init__(self, input_size, value= None):
        self.value = value
        self.column = np.random.rand(input_size)
        self.grad = 0
    
    def get_value(self, input):
        self.value = input @ self.column

class NN_Layer:
    def __init__(self, layer_size, input_size):
        self.nodes = [NN_Node(input_size) for i in layer_size]
    
class NN:
    def __init__(self):
        pass

    def Sequential(self, *layers):
        pass