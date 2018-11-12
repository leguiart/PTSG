# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 09:21:41 2016

@author: stan
"""
from genotype import Genotype
from individual import Individual
from numpy import random
import numpy as np
class Population:
    def __init__(self,environment,parameters,individuals=None):
        self.environment = environment
        self.parameters = parameters
        self.size = self.parameters['n.individuals']
        if individuals==None:
            self.individuals = [self.create_individual() \
            for i in range(0,self.parameters['n.individuals'])]
        else:
            self.individuals = individuals
            self.size = len(individuals)

        
    def create_individual(self):
        if(self.parameters['type']=='permutation'):
            phen = \
            np.array(list(range(0,self.environment.get_chromosome_length())))
            random.shuffle(phen)
            individual = \
            Individual(phenotype=phen)
        else:
            individual = \
            Individual(Genotype(self.environment.get_chromosome_length()))
        return individual
        
    def __str__(self):
        return "\n".join([str(i) for i in self.individuals])
        