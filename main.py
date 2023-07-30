from population import Population


if __name__ == '__main__':
    pop = Population(100)
    x = [
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ]
    output = [0, 1, 1, 0]

    for _ in range(10000):
        for agent in pop.agents:
            agent.fitness = 1
            for i in range(len(x)):
                o = agent.brain.feed_forward(x[i])
                if o[0] == output[i]:
                    agent.fitness *= 10
        best = 0
        for agent in pop.agents:
            agent.fitness /= agent.brain.calculate_weight()
            if agent.fitness > best:
                best = agent.fitness
        print(best)
        pop.natural_selection()
