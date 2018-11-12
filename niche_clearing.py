# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 09:24:59 2016

@author: stan
"""

class NicheClearing:
    
    @staticmethod
    def scale_fitness(population):
        env = population.environment
        sigma = population.parameters['sigma.niche.clearing']/100
        kappa = population.parameters['kappa.niche.clearing']
        
        individuals = sorted(population.individuals,\
        key=lambda x:x.fitness,reverse=True)
        
        for i in range(0,population.size):
            if(individuals[i].fitness>0):
                n_winners = 1
                for j in range(i+1,population.size):
                    if(individuals[j].fitness>0 and \
                    env.compute_normalized_distance(individuals[i],\
                    individuals[j])<sigma):
                        if n_winners < kappa:
                            n_winners = n_winners + 1
                        else:
                            individuals[j].fitness = 0
                            
        