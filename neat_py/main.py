import random

from neat_py.population import Population


def fit(pop: Population):
    for a in pop.agents:
        a.fitness = random.Random().randint(0, 1)


if __name__ == '__main__':
    p = Population(100, 2, 1)
    p.evolve(fit)

