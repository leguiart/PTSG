# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 09:46:33 2016

@author: stan
"""
from decoding_tools import DecodingTools as dt
from environment import Environment
#import numpy as np
class SimpleFunction(Environment):
    function = lambda x:x*x-3*x+6
    #function = lambda x:(x*x-3*x+6)*np.sin(x)/(np.sqrt(1+np.sin(3*x)))
    def evaluate(self,population):
        for individual in population.individuals:
            x = individual.phenotype
            individual.fitness = -SimpleFunction.function(x)
        
    def decode(self,population):
        for individual in population.individuals:
            individual.phenotype = \
            dt.decode_real(individual.genotype.chromosome,0,6,(0.5,0.7))
        
    def get_chromosome_length(self):
        return 6
    