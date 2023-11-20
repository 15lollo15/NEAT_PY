import random

from neat_py.genome import Genome
from neat_py.population import Population

X = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]

Y = [0, 1, 1, 0]


def fit(pop: Population):
    max_f = 0
    for a in pop.agents:
        a.fitness = 4
        for i, x in enumerate(X):
            y = Y[i]
            y_predicted = 1 if a.predict(x)[0] > .5 else 0
            if y != y_predicted:
                a.fitness -= 1
        if a.fitness > max_f:
            max_f = a.fitness
    print(max_f)



if __name__ == '__main__':
    p = Population(100, 2, 1)
    p.evolve_classic(fit)

