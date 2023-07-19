from population import Population


if __name__ == '__main__':
    pop = Population(100)
    input = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ]
    output = [0, 1, 1, 0]

    for _ in range(1000):
        for agent in pop.population:
            agent.fitness = 1
            for i in range(len(input)):
                o = agent.brain.feedForward(input[i])
                if o[0] == output[i]:
                    agent.fitness += 1
        max = 0
        for agent in pop.population:
            if agent.fitness > max:
                max = agent.fitness
        print(max)
        pop.natural_selection()
