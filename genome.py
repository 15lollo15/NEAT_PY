from node import Node
from connection import Connection
from settings import rand_generator
import math

class Genome:
    def __init__(self, inputs, outputs, genome_id, off_spring = False):
        self.inputs = inputs
        self.outputs = outputs
        self.id = genome_id
        self.layers = 2
        self.next_node = 0

        self.nodes = []
        self.connections = []

        if not off_spring:
            for i in range(self.inputs):
                self.nodes.append(Node(self.next_node, 0))
                self.next_node += 1

            for i in range(self.outputs):
                self.nodes.append(Node(self.next_node, 1, True))
                self.next_node += 1

            for i in range(self.inputs):
                for j in range(self.outputs):
                    weight = rand_generator.random() * self.inputs * math.sqrt(2 / self.inputs)
                    self.connections.append(Connection(self.nodes[i], self.nodes[j], weight));

    def generate_network(self):
        for node in self.nodes:
            node.output_connections = []

        for conn in self.connections:
            conn.from_node.output_connections.append(conn)

        self.sort_by_layer();


    def feed_forward(self, input_values):
        self.generate_network()

        for node in self.nodes:
            node.input_sum = 0

        for i in range(self.inputs):
            self.nodes[i].output_value = input_values[i]

        result = [];
        for node in self.nodes:
            node.engage()
            if node.output:
                result.append(node.output_value)

        return result

    def crossover(self, partner):
        off_spring = Genome(self.inputs, self.outputs, 0, True)
        off_spring.next_node = self.next_node

        for i in range(len(self.nodes)):
            node = self.nodes[i].clone()
            if node.output:
                partner_node = partner.nodes[partner.get_node(node.number)]
                if rand_generator.random() > 0.5:
                    node.activation_function = partner_node.activation_function
                    node.bias = partner_node.bias
            off_spring.nodes.append(node);

        for i in range(len(self.connections)):
            index = self.common_connection(self.connections[i].get_innovation_number(), partner.connections)

            if index != -1:
                conn = self.connections[i].clone() if rand_generator.random() > .5 else partner.connections[index].clone()

                from_node = off_spring.nodes[off_spring.get_node(conn.from_node.number)]
                to_node = off_spring.nodes[off_spring.get_node(conn.to_node.number)]
                conn.from_node = from_node
                conn.to_node = to_node

                if from_node is not None and to_node is not None:
                    off_spring.connections.append(conn);
            else:
                conn = self.connections[i].clone();

                from_node = off_spring.nodes[off_spring.get_node(conn.from_node.number)]
                to_node = off_spring.nodes[off_spring.get_node(conn.to_node.number)]
                conn.from_node = from_node
                conn.to_node = to_node

                if from_node is not None and to_node is not None:
                    off_spring.connections.append(conn)

        off_spring.layers = self.layers
        return off_spring

    def mutate(self):
        if rand_generator.random() < 0.8:
            for conn in self.connections:
                conn.mutate_weight()

        if rand_generator.random() < 0.5:
            for node in self.nodes:
                node.mutate_bias()

        if rand_generator.random() < 0.1:
            i = rand_generator.randint(0, len(self.nodes) - 1);
            self.nodes[i].mutate_activation();

        if rand_generator.random() < 0.05:
            self.add_connection()

        if rand_generator.random() < 0.01:
            self.add_node()

    def add_node(self):
        connection_index = rand_generator.randint(0, len(self.connections) - 1);
        picked_connection = self.connections[connection_index];
        picked_connection.enabled = False;
        self.connections.remove(picked_connection)

        new_node = Node(self.next_node, picked_connection.from_node.layer + 1);
        for node in self.nodes:
            if node.layer > picked_connection.from_node.layer:
                node.layer += 1

        new_connection1 = Connection(picked_connection.from_node, new_node, 1);
        new_connection2 = Connection(new_node, picked_connection.to_node, picked_connection.weight);

        self.layers += 1
        self.connections.append(new_connection1)
        self.connections.append(new_connection2)
        self.nodes.append(new_node)
        self.next_node += 1


    def add_connection(self):
        if self.fully_connected():
            return

        node1 = rand_generator.randint(0, len(self.nodes) - 1);
        node2 = rand_generator.randint(0, len(self.nodes) - 1);

        while self.nodes[node1].layer == self.nodes[node2].layer or self.nodes_connected(self.nodes[node1], self.nodes[node2]):
            node1 = rand_generator.randint(0, len(self.nodes) - 1);
            node2 = rand_generator.randint(0, len(self.nodes) - 1);

        if self.nodes[node1].layer > self.nodes[node2].layer:
            temp = node1
            node1 = node2
            node2 = temp

        new_connection = Connection(self.nodes[node1], self.nodes[node2], rand_generator.random() * self.inputs * math.sqrt(2 / self.inputs));
        self.connections.append(new_connection);

    @staticmethod
    def common_connection(inn_n, connections):
        for i in range(len(connections)):
            if inn_n == connections[i].get_innovation_number():
                return i
        return -1


    def nodes_connected(self, node1, node2):
        for i in range(len(self.connections)):
            conn = self.connections[i];
            if (conn.from_node == node1 and conn.to_node == node2) or (conn.from_node == node2 and conn.to_node == node1):
                return True

        return False

    def fully_connected(self):
        max_connections = 0
        nodes_per_layer = {}

        for node in self.nodes:
            if nodes_per_layer.get(node.layer) is not None:
                nodes_per_layer[node.layer] += 1
            else:
                nodes_per_layer[node.layer] = 1

        for i in range(self.layers - 1):
            for j in range(i + 1, self.layers):
                max_connections += nodes_per_layer[i] * nodes_per_layer[j];

        return max_connections == len(self.connections)

    def sort_by_layer(self):
        self.nodes.sort(key=lambda n: n.layer)

    def clone(self):
        clone = Genome(self.inputs, self.outputs, self.id);
        clone.nodes = self.nodes.copy()
        clone.connections = self.connections.copy()
        return clone;


    def get_node(self, x):
        for i in range(len(self.nodes)):
            if self.nodes[i].number == x:
                return i

        return -1


    def calculate_weight(self):
        return len(self.connections) + len(self.nodes)

