import neat_py.connection as connection
from neat_py.neat_settings import Settings
from typing import Callable, List
import math


def sigmoid(x: float) -> float:
    """
    Apply sigmoid
    :rtype: float
    :param x: input value
    :return: the sigmoid of the input value
    """
    return 1 / (1 + math.exp(-4.9 * x))


def identity(x: float) -> float:
    """
    Return the same value that you input
    :rtype: float
    :param x: input value
    :return: the input value
    """
    return x


def step(x: float) -> float:
    """
    Return 1 if the input value is grater than 0, 0 otherwise
    :rtype: float
    :param x: input value
    :return: 1 if the input value is grater than 0, 0 otherwise
    """
    return 1 if x > 0 else 0


def tanh(x: float) -> float:
    """
    Apply tanh
    :rtype: float
    :param x: input value
    :return: the tanh of the input value
    """
    return math.tanh(x)


def relu(x: float) -> float:
    """
    Return 0 if the input value is smaller than 0, the input value otherwise
    :rtype: float
    :param x: input value
    :return: 0 if the input value is smaller than 0, the input value otherwise
    """
    return 0 if x < 0 else x


activations_functions = [
    sigmoid,
    identity,
    step,
    tanh,
    relu
]


def random_float(start: float, end: float) -> float:
    """
    Return a random float between *start* and *end*
    :rtype: float
    :param start: Start value
    :param end: End Value
    :return: A random float between *start* and *end*
    """
    range_size = math.fabs(end - start)
    return Settings.rng.random() * range_size - end


class Node:
    """
    A class that represent a node of a neural network
    """
    def __init__(self, number: int, layer: int, is_output: bool = False) -> None:
        """
        Construct a node with the specified *number*, *layer*
        :param number: Number of the node
        :param layer: Layer of the node inside the network
        :param is_output: Optional parameter to specify that this node is an *output node*
        """
        self.number: int = number
        self.layer: int = layer
        self.is_output: bool = is_output

        self.activation: Callable[[float], float] = Settings.rng.choice(activations_functions)
        self.bias: float = random_float(-1, 1)
        self.input_sum: float = 0.
        self.output_value: float = 0.
        self.output_connections: List[connection.Connection] = []

    def predict(self) -> None:
        if self.layer != 0:
            self.output_value = self.activation(self.input_sum + self.bias)

        for conn in self.output_connections:
            if conn.enabled:
                conn.to_node.input_sum += conn.weight * self.output_value

    def mutate_bias(self) -> None:
        if Settings.rng.random() < Settings.BIAS_RESET_PROBABILITY:
            self.bias = random_float(-1, 1)
        else:
            self.bias += Settings.rng.gauss(0, 1) / 50

    def mutate_activation(self) -> None:
        self.activation = Settings.rng.choice(activations_functions)

    @staticmethod
    def contains(connections: List['connection.Connection'], to_find: 'Node'):
        for conn in connections:
            if conn.to_node == to_find:
                return True
        return False

    def is_connected_to(self, node: 'Node') -> bool:
        if node.layer == self.layer:
            return False

        if node.layer < self.layer:
            return self.contains(node.output_connections, self)
        return self.contains(self.output_connections, node)

    def clone(self) -> 'Node':
        node = Node(self.number, self.layer, self.is_output)
        node.bias = self.bias
        node.activation = self.activation
        return node

