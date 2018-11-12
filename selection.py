# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 10:09:34 2016

@author: stan
"""

from functools import reduce
from numpy import random,sort,cumsum
from random import choice,shuffle
from math import ceil,sqrt
from population import Population
from pareto import Pareto
class Selection:
    @staticmethod
    def tournament(population):
        k = population.parameters['tournament.size']
        return  Population(population.environment, population.parameters,\
        [max([choice(population.individuals) \
        for i in range(0,k)],key=lambda x:x.fitness)\
        for i in range(0,population.size)])
    
    @staticmethod      
    def pareto_tournament(population):
        k = population.parameters['tournament.size']
        fronts = Pareto.fast_non_dominated_sort(population)
        distances = Pareto.crowding_distance(population)
        indices = range(0,population.size)
        membership = Pareto.get_front_membership(fronts)
        individuals = population.individuals
        return Population(population.environment, population.parameters,\
        [individuals[\
        reduce(lambda x,y:\
        Selection.best_crowded_comparison(x,y,membership,distances),\
        [choice(indices) for i in range(0,k)])]\
        for i in range(0,population.size)])

            
    @staticmethod
    def best_crowded_comparison(individual1,individual2,membership,distances):
        if(membership[individual1]<membership[individual2]):
            return individual1
        elif(membership[individual2]<membership[individual1]):
            return individual2
        elif(distances[individual1]>distances[individual2]):
            return individual1
        else:
            return individual2
            
    @staticmethod
    def roulettewheel(population):
        pointers = sort(random.uniform(size=population.size))
        total_fitness = reduce(lambda x,y:x+y, \
        map(lambda i:i.fitness,population.individuals))
        probabilities = map(lambda x:x.fitness/total_fitness, \
        population.individuals)
        selected = []
        delimiters = cumsum(list(probabilities))
        
        i_p = 0
        i_d = 0
        while i_p < population.size and i_d < population.size:
            while i_p < population.size and pointers[i_p] < delimiters[i_d]:
                selected=selected+[population.individuals[i_d]]
                i_p = i_p + 1
            i_d = i_d + 1
        shuffle(selected)
        return  Population(population.environment, population.parameters,\
        selected)
        
    @staticmethod
    def ranking(population):
        n = population.size
        pointers = random.uniform(1,(n*(n+1))>>1,n)
        population.individuals.sort(key=lambda x: x.fitness)
        selected = [population.individuals[\
        int(ceil((-1 + sqrt(1+8*p))/2))-1] for p in pointers]
        return  Population(population.environment, population.parameters,\
        selected)
        
    @staticmethod
    def pareto_crowded(population):
        fronts = Pareto.fast_non_dominated_sort(population)
        distances = Pareto.crowding_distance(population)
        front = 0
        selected = []
        while(len(selected)+len(fronts[front])<(population.size>>1)):
            selected = selected + \
            [population.individuals[i] for i in fronts[front]]
            front = front + 1
            
        n = (population.size>>1) - len(selected)
        
        distances_last_front = [(distances[i],population.individuals[i]) \
        for i in fronts[front]]
        sorted_distances = sorted(distances_last_front,key=lambda x:x[0],\
        reverse=True)
        selected = selected + [i[1] for i in sorted_distances[:n]]   
        
        return \
        Population(population.environment,population.parameters,selected)
            
            
            
            
            
            
            
            
            