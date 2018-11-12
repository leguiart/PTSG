# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 09:46:33 2016

@author: stan
"""
from environment import Environment
class Ones(Environment):
    def evaluate(self,population):
        for individual in population.individuals:
            individual.fitness = individual.phenotype
        
    def get_gene_template(self):
        return [([10,0])]
        
    def decode(self,population):
        for individual in population.individuals:
            individual.phenotype = individual.genotype.chromosome
        
    def get_chromosome_length(self):
        return 10
    