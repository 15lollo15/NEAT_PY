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

    for _ in range(10000):
        for agent in pop.agents:
            agent.fitness = 1
            for i in range(len(input)):
                o = agent.brain.feed_forward(input[i])
                if o[0] == output[i]:
                    agent.fitness *= 10
        max = 0
        for agent in pop.agents:
            agent.fitness /= agent.brain.calculate_weight()
            if agent.fitness > max:
                max = agent.fitness
        print(max)
        pop.natural_selection()
