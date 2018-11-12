from env_ones import  Ones
from ga import GeneticAlgorithm

e  = Ones()

par = {"crossover.type" : "single",
        "elitism" : False,
        "n.generations" : 100,
        "n.individuals" : 100,
        "p.crossover" : 0.8,
        "p.mutation" : 0.01,
        "selection.type" : "tournament.selection",
        "tournament.size" : 2,
        "type" : "simple"}

g = GeneticAlgorithm(e, par)

print (g.population)

g.evolve()

print (g.population)
