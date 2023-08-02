from population import Population


def my_fitness_function(pop: Population):
    x = [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1]
        ]
    output = [0, 1, 1, 0]
    for agent in pop.agents:
        agent.fitness = 1
        for i in range(len(x)):
            o = agent.brain.predict(x[i])
            if o[0] == output[i]:
                agent.fitness += 1
    best = 0
    for agent in pop.agents:
        #agent.fitness /= agent.brain.calculate_weight()
        if agent.fitness > best:
            best = agent.fitness
    print(best)


if __name__ == '__main__':
    pop = Population(100, 2, 1)
    pop.evolve(my_fitness_function)
