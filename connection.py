from settings import rand_generator


class Connection:
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.enabled = True

    def mutate_weight(self):
        rand = rand_generator.random()
        if rand < 0.05:
            self.weight = rand_generator.random() * 2 - 1
        else:
            self.weight += rand_generator.gauss(0, 1) / 50

    def clone(self):
        clone = Connection(self.from_node, self.to_node, self.weight)
        clone.enabled = self.enabled
        return clone

    def get_innovation_number(self):  # Using https://en.wikipedia.org/wiki/Pairing_function#Cantor_pairing_function
        return (1 / 2) * (self.from_node.number + self.to_node.number) * (
                self.from_node.number + self.to_node.number + 1) + self.to_node.number
