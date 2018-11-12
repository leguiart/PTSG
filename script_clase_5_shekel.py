from ga import*
from shekel import*


par = {"crossover.type" : "single",
        "elitism" : False,
        "n.generations" : 100,
        "n.individuals" : 100,
        "p.crossover" : 0.8,
        "p.mutation" : 0.01,
        "selection.type" : "tournament.selection",
        "tournament.size" : 2,
        "type" : "simple"}


"""
par = {"crossover.type" : "single",
        "elitism" : True,
        "n.generations" : 100,
        "n.individuals" : 100,
        "p.crossover" : 0.8,
        "p.mutation" : 0.01,
        "selection.type" : "tournament.selection",
        "tournament.size" : 2,
        "type" : "simple"
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

s = Shekel()
#s.show()
ga = GeneticAlgorithm(s , par)
print(ga.population)
ga.evolve()
#print(ga.population)
s.show(ga.population)
