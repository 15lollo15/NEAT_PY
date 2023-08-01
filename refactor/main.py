from refactor.population import Population
from settings import rng

pop = Population(100, 2, 1)

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
            o = agent.brain.predict(x[i])
            if o[0] == output[i]:
                agent.fitness += 1
    best = 0
    for agent in pop.agents:
        #agent.fitness /= agent.brain.calculate_weight()
        if agent.fitness > best:
            best = agent.fitness
    print(best)
    # if best == 5:
    #     exit()
    pop.natural_selection()
