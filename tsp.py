from environment import Environment
from local import LocalSearchProblem
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt
import random
class TSP(Environment, LocalSearchProblem):
    def __init__(self,n=10,interactive=False):
        self.n = n
        self.interactive = interactive

        #generate random cities
        self.cities = np.random.uniform(size=(n,2))
        if(interactive):
            plt.ion()

    def evaluate(self,population):
        for individual in population.individuals:
            individual.fitness = 1/self.compute_cost(individual.phenotype)

    def decode(self,population):
        return

    def get_chromosome_length(self):
        return self.n

    def compute_cost(self,permutation):
        n = len(list(permutation))
        M = self.cities[permutation,:]
        return np.sum(np.sqrt(np.sum(\
        (M-M[[i%n for i in range(1,n+1)],:])**2,axis=1)))

    @staticmethod
    def compute_distance(individual1,individual2):
        return np.count_nonzero(individual1.phenotype-individual2.phenotype)

    def compute_normalized_distance(self,individual1,individual2):
        return TSP.compute_distance(individual1,individual2)/self.n

    def show(self,population,colors='blue',clear=False):
        if(clear):
            plt.clf()
        best = min(population.individuals,\
        key=lambda i:self.compute_cost(i.phenotype))
        M = self.cities[best.phenotype,:]
        X = M[[i%self.n for i in range(0,self.n+1)],0]
        Y = M[[i%self.n for i in range(0,self.n+1)],1]
        plt.scatter(X,Y,color = 'red',marker="o")
        plt.plot(X,Y,color=colors)
        plt.title('best individual, cost='+\
        str(self.compute_cost(best.phenotype)))

        plt.grid()
        if(self.interactive):
            plt.pause(1)
        else:
            plt.show()

    def aleatoria(self):
        conf = random.sample(range(self.n), self.n)
        return conf

    def energia(self, x):
        return self.compute_cost(x)

    def move(self, x):
        i = random.randint(0, self.n -1)
        j = random.randint(0, self.n -1)
        k = x[i]
        x[i] = x[j]
        x[j] = k
        return x

    def energiaPromedio(self):
        li = [[self.compute_cost(random.sample(range(self.n), self.n)) for i in range(int(self.n*3))]\
        [j%(self.n*3)] for j in range(1, self.n*3+1)]
        return sum([np.abs(li[i]-li[i-1]) for i in range(1,len(li))])/(len(li)-1)

    def showSA(self, x):
        plt.clf()
        M = self.cities[x,:]
        X = M[[i%self.n  for i in range(0, self.n +1)],0]
        Y = M[[i%self.n  for i in range(0, self.n +1)],1]
        plt.scatter(X,Y,color = 'red', marker = "o")
        plt.plot(X,Y,color = 'blue')
        plt.title('mejor solucion, costo='+str(self.energia(x)))
        plt.grid()
        plt.pause(5)
