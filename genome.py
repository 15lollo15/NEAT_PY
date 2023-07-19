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
        self.nextNode = 0

        self.nodes = []
        self.connections = []

        if not off_spring:
            for i in range(self.inputs):
                self.nodes.append(Node(self.nextNode, 0))
                self.nextNode += 1

            for i in range(self.outputs):
                self.nodes.append(Node(self.nextNode, 1, True))
                self.nextNode += 1

            for i in range(self.inputs):
                for j in range(self.outputs):
                    weight = rand_generator.random() * self.inputs * math.sqrt(2 / self.inputs)
                    self.connections.append(Connection(self.nodes[i], self.nodes[j], weight));

    def generate_network(self):
        for node in self.nodes:
            node.output_connections = []

        for conn in self.connections:
            conn.fromNode.output_connections.append(conn)

        self.sortByLayer();


    def feedForward(self, input_values):
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
        offSpring = Genome(self.inputs, self.outputs, 0, True)
        offSpring.nextNode = self.nextNode

        for i in range(len(self.nodes)):
            node = self.nodes[i].clone()
            if node.output:
                partnerNode = partner.nodes[partner.getNode(node.number)]
                if rand_generator.random() > 0.5:
                    node.activation_function = partnerNode.activation_function
                    node.bias = partnerNode.bias
            offSpring.nodes.append(node);

        maxLayer = 0;
        for i in range(len(self.connections)):
            index = self.commonConnection(self.connections[i].get_innovation_number(), partner.connections)

            if index != -1:
                conn = self.connections[i].clone() if rand_generator.random() > .5 else partner.connections[index].clone()

                fromNode = offSpring.nodes[offSpring.getNode(conn.fromNode.number)]
                toNode = offSpring.nodes[offSpring.getNode(conn.toNode.number)]
                conn.fromNode = fromNode
                conn.toNode = toNode

                if fromNode is not None and toNode is not None:
                    offSpring.connections.append(conn);
            else:
                conn = self.connections[i].clone();

                fromNode = offSpring.nodes[offSpring.getNode(conn.fromNode.number)]
                toNode = offSpring.nodes[offSpring.getNode(conn.toNode.number)]
                conn.fromNode = fromNode
                conn.toNode = toNode

                if fromNode is not None and toNode is not None:
                    offSpring.connections.append(conn)

        offSpring.layers = self.layers
        return offSpring

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
            self.addConnection()

        if rand_generator.random() < 0.01:
            self.addNode()

    def addNode(self):
        connectionIndex = rand_generator.randint(0, len(self.connections) - 1);
        pickedConnection = self.connections[connectionIndex];
        pickedConnection.enabled = False;
        self.connections.remove(pickedConnection)

        newNode = Node(self.nextNode, pickedConnection.fromNode.layer + 1);
        for node in self.nodes:
            if node.layer > pickedConnection.fromNode.layer:
                node.layer += 1

        newConnection1 = Connection(pickedConnection.fromNode, newNode, 1);
        newConnection2 = Connection(newNode, pickedConnection.toNode, pickedConnection.weight);

        self.layers += 1
        self.connections.append(newConnection1)
        self.connections.append(newConnection2)
        self.nodes.append(newNode)
        self.nextNode += 1


    def addConnection(self):
        if self.fullyConnected():
            return

        node1 = rand_generator.randint(0, len(self.nodes) - 1);
        node2 = rand_generator.randint(0, len(self.nodes) - 1);

        while self.nodes[node1].layer == self.nodes[node2].layer or self.nodesConnected(self.nodes[node1], self.nodes[node2]):
            node1 = rand_generator.randint(0, len(self.nodes) - 1);
            node2 = rand_generator.randint(0, len(self.nodes) - 1);

        if self.nodes[node1].layer > self.nodes[node2].layer:
            temp = node1
            node1 = node2
            node2 = temp

        newConnection = Connection(self.nodes[node1], self.nodes[node2], rand_generator.random() * self.inputs * math.sqrt(2 / self.inputs));
        self.connections.append(newConnection);

    def commonConnection(self, innN, connections):
        for i in range(len(connections)):
            if innN == connections[i].get_innovation_number():
                return i
        return -1


    def nodesConnected(self, node1, node2):
        for i in range(len(self.connections)):
            conn = self.connections[i];
            if (conn.fromNode == node1 and conn.toNode == node2) or (conn.fromNode == node2 and conn.toNode == node1):
                return True

        return False

    def fullyConnected(self):
        maxConnections = 0
        nodesPerLayer = {}

        for node in self.nodes:
            if nodesPerLayer.get(node.layer) != None:
                nodesPerLayer[node.layer] += 1
            else:
                nodesPerLayer[node.layer] = 1

        for i in range(self.layers - 1):
            for j in range(i + 1, self.layers):
                maxConnections += nodesPerLayer[i] * nodesPerLayer[j];

        return maxConnections == len(self.connections)

    def sortByLayer(self):
        self.nodes.sort(key=lambda n: n.layer)

    def clone(self):
        clone = Genome(self.inputs, self.outputs, self.id);
        clone.nodes = self.nodes.copy()
        clone.connections = self.connections.copy()
        return clone;


    def getNode(self, x):
        for i in range(len(self.nodes)):
            if self.nodes[i].number == x:
                return i

        return -1


    def calculateWeight(self):
        return self.connections.length + self.nodes.length

