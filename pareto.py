# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 10:34:34 2016

@author: stan
"""
import math
import numpy as np
class Pareto:
    
    @staticmethod
    def fast_non_dominated_sort(population):
        fronts = [[]]
        S = [[] for i in range(0, population.size)]
        n = [0]*population.size
        individuals = population.individuals
        for i in range(0, population.size):
            for j in range(i+1,population.size):
                dominance = \
                Pareto.dominates(individuals[i],individuals[j],\
                population.environment)
                if(dominance[0]):
                    S[i].append(j)
                    n[j] = n[j] + 1
                elif(dominance[1]):
                    S[j].append(i)
                    n[i] = n[i] + 1
            if(n[i]==0):
                fronts[0].append(i)
        i = 0
        while(fronts[i]):
            H = []
            for p in fronts[i]:
                for q in S[p]:
                    n[q] = n[q]-1
                    if(n[q]==0):
                        H.append(q)
            i = i + 1
            fronts.append(H)
        fronts.pop()
        return fronts
        
    @staticmethod
    def get_front_membership(fronts):
        membership={}
        for i in range(0,len(fronts)):
            for j in fronts[i]:
                membership[j] = i
        return membership
            
    @staticmethod
    def crowding_distance(population):
        l = population.size
        distances = [0]*population.size
        n = population.environment.get_number_of_objectives()
        for i in range(0,n):
            I = sorted(enumerate(population.individuals),\
            key = lambda x:x[1].objectives[i])
            distances[I[0][0]] = math.inf
            distances[I[l-1][0]] = math.inf
            for j in range(1,l-1):
                distances[I[j][0]] = distances[I[j][0]] + \
                (population.individuals[I[j+1][0]].objectives[i] - \
                 population.individuals[I[j-1][0]].objectives[i])
        return distances
                 
                
    @staticmethod
    def dominates(individual1,individual2,environment):
        
        # array in {-1,+1}; -1 minimization, +1 maximization
        direction = environment.get_optimization_type()
        x1 = np.multiply(individual1.objectives,direction)
        x2 = np.multiply(individual2.objectives,direction)

        diff = x1 - x2

        negative = np.where(diff<0)[0]
        positive = np.where(diff>0)[0]

        dom_1_2 = (False if(len(negative)>0) else len(positive)>0)
        dom_2_1 = (False if(len(positive)>0) else len(negative)>0)
        

        
        return [dom_1_2,dom_2_1]
        
        
        
        