from tsp import TSP
from SA import SimulatedAnnealing
from ga import GeneticAlgorithm
#import numpy as np
tsp = TSP(20, True)
tsp.showSA(list(range(0,20)))
"""
lst = []
l = list(range(0,20))
for i in range(40):
    x = tsp.energia(l)
    l = tsp.move(l)
    lst.append(np.abs(tsp.energia(l)-x))
print(np.mean(lst))
print(np.std(lst))
"""
par = {"crossover.type" : "permutation.ox",
        "elitism" : True,
        "n.generations" : 100,
        "n.individuals" : 100,
        "p.crossover" : 0.8,
        "p.mutation" : 0.1,
        "selection.type" : "tournament.selection",
        "tournament.size" : 4,
        "type" : "permutation"}


#Con estos parámetros nunca encuentra la solución, porque el mutation rate es muy bajo, no es elitista, y el tamaño del torneo es demasiado bajo
"""
par = {"crossover.type" : "permutation.ox",
        "elitism" : False,
        "n.generations" : 100,
        "n.individuals" : 100,
        "p.crossover" : 0.8,
        "p.mutation" : 0.01,
        "selection.type" : "tournament.selection",
        "tournament.size" : 2,
        "type" : "permutation"
        }
"""
"""
par = {"crossover.type" : "single",
        "elitism" : False,
        "n.generations" : 100,
        "n.individuals" : 100,
        "p.crossover" : 0.8,
        "p.mutation" : 0.01,
        "selection.type" : "tournament.selection",
        "tournament.size" : 2,
        "type" : "simple",
        "sharing.domain" : "phenotype",
        "alpha.share" : 1,
        "theta.share" : 0.1,
        "fitness.sharing" : True
        }
"""

prom = tsp.energiaPromedio()
sa = SimulatedAnnealing(tsp)
best = list(sa.search(0.999, prom, prom/1000, 100)[0])
tsp.showSA(best)

tsp = TSP(20, True)
ga = GeneticAlgorithm(tsp, par)
tsp.show(ga.population)
print(ga.population)
ga.evolve()
tsp.show(ga.population)


