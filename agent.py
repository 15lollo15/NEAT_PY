from genome import Genome


class Agent:
    def __init__(self, agent_id: int, num_input: int, num_output: int):
        self.brain = Genome(num_input, num_output, agent_id)
        self.num_input = num_input
        self.num_output = num_output
        self.fitness = 0
        self.agent_id = agent_id

    def crossover(self, parent):
        child = Agent(1, self.num_input, self.num_output)
        if parent.fitness < self.fitness:
            child.brain = self.brain.crossover(parent.brain)
        else:
            child.brain = parent.brain.crossover(self.brain)

        child.brain.mutate()
        return child
