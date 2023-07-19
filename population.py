from agent import Agent
from settings import *

class Population:
    def __init__(self, size):
        self.population = []

        for i in range(size):
            self.population.append(Agent(i, 2, 1))
            self.population[i].brain.generate_network()
            self.population[i].brain.mutate()

    def max_fitness(self):
        max_f = 0
        for agent in self.population:
            if agent.fitness > max_f:
                max_f = agent.fitness
        return max_f

    def natural_selection(self):
        max_f = self.max_fitness();
        for agent in self.population:
            agent.fitness /= max_f

        pool = []
        for i in range(len(self.population)):
            n = int(self.population[i].fitness * 100)
            for _ in range(n):
                pool.append(i)

        children = []
        for i in range(len(self.population)):
            parent1_index = pool[rand_generator.randint(0, len(self.population) - 1)]
            parent2_index = pool[rand_generator.randint(0, len(self.population) - 1)]
            parent1 = self.population[parent1_index]
            parent2 = self.population[parent2_index]
            if parent1.fitness > parent2.fitness:
                children.append(parent1.crossover(parent2))
            else:
                children.append(parent2.crossover(parent1))

        self.population = children