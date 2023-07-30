from settings import rand_generator
import math

activationsNames = ["Sigmoid", "Identity", "Step", "Tan", "ReLu"]


class Node:
    def __init__(self, num, lay, is_output=False):
        self.number = num
        self.layer = lay
        self.activation_function = rand_generator.randint(0, 4)
        self.bias = rand_generator.random() * 2 - 1
        self.output = is_output

        self.input_sum = 0
        self.output_value = 0
        self.output_connections = []

    def engage(self):
        if self.layer != 0:
            self.output_value = self.activation(self.input_sum + self.bias)

        for conn in self.output_connections:
            if conn.enabled:
                conn.to_node.input_sum += conn.weight * self.output_value

    def mutate_bias(self):
        rand = rand_generator.random()
        if rand < 0.05:
            self.bias = rand_generator.random() * 2 - 1
        else:
            self.bias += rand_generator.gauss(0, 1) / 50

    def mutate_activation(self):
        self.activation_function = rand_generator.randint(0, 4)

    def is_connected_to(self, node):
        if node.layer == self.layer:
            return False

        if node.layer < self.layer:
            for conn in node.output_connections:
                if conn.to_node == self:
                    return True
        else:
            for conn in self.output_connections:
                if conn.to_node == node:
                    return True

        return False

    def clone(self):
        node = Node(self.number, self.layer, self.output)
        node.bias = self.bias
        node.activation_function = self.activation_function
        return node

    def activation(self, x):
        if self.activation_function == 0:  # Sigmoid
            return 1 / (1 + math.exp(-4.9 * x))
        if self.activation_function == 1:  # Identity
            return x
        if self.activation_function == 2:  # Step
            return 1 if x > 0 else 0
        if self.activation_function == 3:  # Tan
            return math.tanh(x)
        if self.activation_function == 4:  # ReLu
            return 0 if x < 0 else x
        return 1 / (1 + math.exp(-4.9 * x))
